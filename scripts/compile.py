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
                         'print(f"Initial tape:")',
                         'print("".join(tape))\n',
                         "io_head_index = 2"])

        # Execution block
        indent_num = 0
        indent = "    "
        loop_stack = []
        for i, command in enumerate(self.commands):
            if command == "#":  # Won't parse anything after "#"
                break
            elif command == 'I':
                template.append(indent_num * indent + 'print("".join(tape))')
            elif command == '0':
                template.append(indent_num * indent + 'tape[io_head_index] = "0"')
            elif command == '1':
                template.append(indent_num * indent + 'tape[io_head_index] = "1"')
            elif command == 'D':
                template.append(indent_num * indent + "io_head_index += 1")
            elif command == 'G':
                template.append(indent_num * indent + "io_head_index -= 1")
            elif command == "si":
                condition = self.commands[i + 1][1]  # "0" or "1"
                template.append(indent_num * indent + f"if tape[io_head_index] == '{condition}':")
                indent_num += 1
            elif command in ["(0)", "(1)"]:  # Already parsed with "si"
                pass
            elif command == "boucle":
                template.append(indent_num * indent + "while True:")
                indent_num += 1
                loop_stack.append("boucle")
            elif command == "}":
                indent_num -= 1
            elif command == "fin":
                if not loop_stack:
                    template.append(indent_num * indent + "quit()")
                template.append(indent_num * indent + "break")
            else:
                raise Exception(f"Invalid command: {command}")

        template += ['print(f"Final tape:")',
                     'print("".join(tape))\n']

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

    parser = argparse.ArgumentParser(description="A Python-based TS script compiler.")
    parser.add_argument("-s", "--script",
                        default=Path("../ts_scripts/addition.1.TS"),
                        type=Path,
                        metavar="",
                        help="TS script to compile. Default set to addition script")
    args = parser.parse_args()

    main(args.script)
