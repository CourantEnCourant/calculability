""""""
import logging
from pathlib import Path
from typing import Sequence, Optional


class Compiler:
    def __init__(self):
        self.commands = []

    def read_clean(self, ts_file: Path):
        # Read and strip comment
        with open(ts_file) as f:
            file_lines = f.readlines()
            command_lines = []
            for line in file_lines:
                line = self.__strip_comment(line)
                command_lines.append(line)
            commands = " ".join(command_lines)
            commands = commands.split()
        # Check invalid command
        valid_commands = ["I", "P", "D", "G", "1", "0", "si", "(0)", "(1)", "boucle", "fin", "}", "#"]
        for command in commands:
            if command not in valid_commands:
                raise Exception(f"Invalid command: {command}")
        self.commands = commands

    def __strip_comment(self, command_line: str) -> str:
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
        # Check if script ends by "#"
        if self.commands[-1] != "#":
            raise Exception('Script should end with "#"')
        # Check "si" followed by "(x)"
        for i, command in enumerate(self.commands):
            try:
                if command == "si" and self.commands[i + 1] not in ["(0)", "(1)"]:
                    flag = False
                    print('"si" and (x) not matching')
            except Exception as e:
                raise Exception(e)
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
                except Exception:
                    flag = False
                    print("Curly brackets not matching")
        if syntax_stack:
            flag = False
            print("Curly brackets not matching.")
        return flag

    def compile(self, output_file: Path):
        if not self.check_grammar():
            raise Exception(f"Syntax error")
        # `sys` module
        template = ["import sys",
                    "args = sys.argv[1:]\n"]
        # Generate tape
        template.extend(['tape = ["0", "0"]',
                         "for arg in args:",
                         '    tape += ["1" for _ in range(int(arg) + 1)] + ["0", "0"]\n',
                         'if len(tape) <= 50:',
                         '    tape = tape + ["0" for _ in range(50 - len(tape))]\n',
                         "io_head_index = 2"])
        # show_tape() function
        template.extend(["show_tape_index = 0",
                         "\n\ndef show_tape():",
                         "    global tape, show_tape_index",
                         "    if show_tape_index < len(tape):",
                         '        print(tape[show_tape_index], end="")',
                         "        show_tape_index += 1",
                         "        show_tape()",
                         "    else:",
                         '        print("")',
                         "        show_tape_index = 0\n\n"])
        # Parse "boucle" for global variables
        boucle_count = sum([1 for command in self.commands if command == "boucle"])
        for i in range(boucle_count):
            template.append(f"in_loop_{i + 1} = True")
        # Print initial tape
        template.extend(['\nprint(f"Initial tape:")',
                         'show_tape()\n'])
        # Execution block
        indent_num = 0
        indent = "    "
        command_stack = []
        loop_stack = []
        loop_count = 0
        for i, command in enumerate(self.commands):
            if command == "#":  # Won't parse anything after "#"
                break
            elif command == 'I':
                template.append(indent_num * indent + 'show_tape()')
            elif command == '0':
                template.append(indent_num * indent + 'tape[io_head_index] = "0"')
                # template.append(indent_num * indent + 'print("".join([" "] * io_head_index + ["X"]) + "    Changed to 0")')
                # template.append(indent_num * indent + 'show_tape()')
            elif command == '1':
                template.append(indent_num * indent + 'tape[io_head_index] = "1"')
                # template.append(indent_num * indent + 'print("".join([" "] * io_head_index + ["X"]) + "    Changed to 1")')
                # template.append(indent_num * indent + 'show_tape()')
            elif command == 'D':
                template.append(indent_num * indent + "io_head_index += 1")
                # template.append(indent_num * indent + 'print(io_head_index)')
                # template.append(indent_num * indent + 'print("".join([" "] * io_head_index + ["X"]))')
                # template.append(indent_num * indent + 'show_tape()')
            elif command == 'G':
                template.append(indent_num * indent + "io_head_index -= 1")
                # template.append(indent_num * indent + 'print(io_head_index)')
                # template.append(indent_num * indent + 'print("".join([" "] * io_head_index + ["X"]))')
                # template.append(indent_num * indent + 'show_tape()')
            elif command == "si":
                condition = self.commands[i + 1][1]  # "0" or "1"
                template.append(indent_num * indent + f"if tape[io_head_index] == '{condition}':")
                indent_num += 1  # "si" indent
                command_stack.append(command)
            elif command in ["(0)", "(1)"]:  # Already parsed with "si"
                pass
            elif command == "boucle":
                command_stack.append(command)
                loop_count += 1
                loop_stack.append(loop_count)
                template.append(indent_num * indent + f"def loop_{loop_count}():")
                indent_num += 1  # Function definition indent
                template.append(indent_num * indent + f"global in_loop_{loop_count}, tape, io_head_index")
                template.append(indent_num * indent + f"if in_loop_{loop_count}:")
                indent_num += 1  # Function recursive-call indent
            elif command == "}":
                match_command = command_stack.pop()
                if match_command == "si":
                    indent_num -= 1
                    continue
                elif match_command == "boucle":
                    current_loop_count = loop_stack.pop()
                    template.append(indent_num * indent + f"loop_{current_loop_count}()")  # Recursive call
                    indent_num -= 2
                    template.append(indent_num * indent + f"loop_{current_loop_count}()")  # Function execution
                else:
                    raise Exception("Illegal command in command stack")
            elif command == "fin":
                if not loop_stack:
                    template.append(indent_num * indent + "quit()")
                else:
                    # loop_stack.pop()
                    current_loop_count = loop_stack[-1]
                    # template.append(indent_num * indent + f"in_loop_{current_loop_count} = False")
                    template.append(indent_num * indent + "return None")
            else:
                raise Exception(f"Invalid command: {command}")

        template += ['print(f"Final tape:")',
                     'show_tape()\n']

        final_code = "\n".join(template)
        with open(output_file, 'w') as file:
            file.write(final_code)
        print(f"MTdv code succesfully compiled to {output_file}")


def main(script: Path):
    # Logger config
    logging.basicConfig(level=logging.INFO)
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
