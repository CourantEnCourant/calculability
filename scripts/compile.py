""""""
from pathlib import Path


class Compiler:
    def __init__(self):
        self.commands = []
        self.template = []
        self.indent_num = 0
        self.indent = "    "
        self.command_stack = []
        self.loop_stack = []
        self.loop_count = 0
        self.command_index = 0
        self.command2func = {"I": self.__evaluate_I,
                             "0": self.__evaluate_0,
                             "1": self.__evaluate_1,
                             "D": self.__evaluate_D,
                             "G": self.__evaluate_G,
                             "si": self.__evaluate_si,
                             "boucle": self.__evaluate_boucle,
                             "fin": self.__evaluate_fin,
                             "}": self.__evaluate_right_bracket,
                             "(0)": self.__evaluate_si_0_or_1,
                             "(1)": self.__evaluate_si_0_or_1}

    def read_clean(self, ts_file: Path):
        # Read and strip comment
        with open(ts_file) as f:
            file_lines = f.readlines()
            command_lines = []
            for line in file_lines:
                line = Compiler.strip_comment(line)
                command_lines.append(line)
            commands = " ".join(command_lines)
            commands = commands.split()
        # Check invalid command
        valid_commands = ["I", "P", "D", "G", "1", "0", "si", "(0)", "(1)", "boucle", "fin", "}", "#"]
        for command in commands:
            if command not in valid_commands:
                raise Exception(f"Invalid command: {command}")
        self.commands = commands

    @staticmethod
    def strip_comment(command_line: str) -> str:
        """Inner method for self.read_clean()"""
        new_line = command_line
        for i, symbol in enumerate(command_line):
            if symbol == "%":
                new_line = command_line[:i]
                break
        return new_line

    def check_grammar(self):
        if not self.commands:
            raise Exception(f"No commands found")
        flag = True
        # Check "si" followed by "(x)"
        for i, command in enumerate(self.commands):
            if command == "si" and self.commands[i + 1] not in ["(0)", "(1)"]:
                flag = False
                print('"si" and (x) not matching')
        # Check curly brackets matching
        syntax_stack = []
        for command in self.commands:
            if command == "boucle":
                syntax_stack.append(command)
            if command == "si":
                syntax_stack.append(command)
            if command == "}":
                try:
                    syntax_stack.pop()
                except IndexError:
                    flag = False
                    print("Curly brackets not matching")
        if syntax_stack:
            flag = False
            print("Curly brackets not matching.")
        return flag

    def __evaluate_I(self):
        self.template.append(self.indent_num * self.indent + 'show_tape()')
        self.command_index += 1

    def __evaluate_0(self):
        self.template.append(self.indent_num * self.indent + 'tape[io_head_index] = "0"')
        self.command_index += 1

    def __evaluate_1(self):
        self.template.append(self.indent_num * self.indent + 'tape[io_head_index] = "1"')
        self.command_index += 1

    def __evaluate_D(self):
        self.template.append(self.indent_num * self.indent + "io_head_index += 1")
        self.command_index += 1

    def __evaluate_G(self):
        self.template.append(self.indent_num * self.indent + "io_head_index -= 1")
        self.command_index += 1

    def __evaluate_si(self):
        condition = self.commands[self.command_index + 1][1]  # "0" or "1"
        self.template.append(self.indent_num * self.indent + f"if tape[io_head_index] == '{condition}':")
        self.indent_num += 1  # "si" indent
        self.command_stack.append("si")
        self.command_index += 1

    def __evaluate_si_0_or_1(self):
        """Already parsed by 'si'"""
        self.command_index += 1

    def __evaluate_right_bracket(self):
        match_command = self.command_stack.pop()
        if match_command == "si":
            self.indent_num -= 1
        elif match_command == "boucle":
            current_loop_count = self.loop_stack.pop()
            self.template.append(self.indent_num * self.indent + f"return loop_{current_loop_count}(tape, io_head_index)")  # Recursive call
            self.indent_num -= 1
            self.template.append(self.indent_num * self.indent + f"tape, io_head_index = loop_{current_loop_count}(tape, io_head_index)")  # Function execution
        self.command_index += 1

    def __evaluate_boucle(self):
        self.command_stack.append("boucle")
        self.loop_count += 1
        self.loop_stack.append(self.loop_count)
        self.template.append(self.indent_num * self.indent + f"def loop_{self.loop_count}(tape, io_head_index):")
        self.indent_num += 1  # Function definition indent
        self.command_index += 1

    def __evaluate_fin(self):
        if not self.loop_stack:
            self.template.append(self.indent_num * self.indent + "quit()")
        else:
            self.template.append(self.indent_num * self.indent + "return tape, io_head_index")
        self.command_index += 1

    def __create_template_head(self):
        # `sys` module
        self.template = ["import sys",
                         "args = sys.argv[1:]\n"]
        # Generate tape
        self.template.extend(['tape = ["0", "0"]',
                              'for arg in args:',
                              '    tape += ["1" for _ in range(int(arg) + 1)] + ["0", "0"]\n',
                              'if len(tape) <= 50:',
                              '    tape = tape + ["0" for _ in range(50 - len(tape))]\n',
                              "io_head_index = 2"])

        # show_tape() function
        self.template.extend(["show_tape_index = 0",
                              "\n\ndef show_tape():",
                              "    global tape, show_tape_index",
                              "    if show_tape_index < len(tape):",
                              '        print(tape[show_tape_index], end="")',
                              "        show_tape_index += 1",
                              "        show_tape()",
                              "    else:",
                              '        print("")',
                              "        show_tape_index = 0\n\n"])

        # Print initial tape
        self.template.extend(['print(f"Initial tape:")',
                              'show_tape()\n'])

    def __count_loop_global_var(self):
        """Count "boucle" to generate enough `in_loop_num = True` global variables"""
        boucle_count = sum([1 for command in self.commands if command == "boucle"])
        for i in range(boucle_count):
            self.template.append(f"in_loop_{i + 1} = True")

    def __output(self, output_file):
        # Print final tape
        self.template += ['print(f"Final tape:")',
                          'show_tape()\n']
        # Output to file
        final_code = "\n".join(self.template)
        with open(output_file, 'w') as file:
            file.write(final_code)
        print(f"MTdv code successfully compiled to {output_file}")

    def compile(self, output_file: Path):
        if not self.check_grammar():
            raise Exception(f"Syntax error")
        # Preparation
        self.__create_template_head()

        # Compilation
        for command in self.commands:
            if command == "#":
                break
            else:
                self.command2func[command]()

        self.__output(output_file)


def main(script: Path):
    # Compiler preparation
    compiler = Compiler()
    compiler.read_clean(script)
    # Compilation
    output_stem = script.stem
    output_path = Path(f"../exec/{output_stem}.py")
    compiler.compile(output_path)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="A Python-based TS script compiler")
    parser.add_argument("script",
                        type=Path,
                        help="TS script to compile")
    args = parser.parse_args()

    main(args.script)
