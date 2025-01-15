from dataclasses import dataclass


@dataclass
class Command:
    # As programming languages are CFLs, they are trees
    index: int
    value: str
    left: "Command" = None
    right: "Command" = None  # Only for double-node

    def __repr__(self):
        """Add restriction to avoid recursive representation"""
        left_info = None
        right_info = None
        if self.left is not None:
            left_info = f"{self.left.index, self.left.value}"
        if self.right is not None:
            right_info = f"{self.right.index, self.right.value}"
        return f"Current: {self.index, self.value}. Left: {left_info}. Right: {right_info}"


class TuringMachine:
    def __init__(self, tape_length=80, allowing_step=9999):
        self.tape = []
        self.commands = []
        self.tape_length = tape_length
        self.allowing_step = allowing_step  # Detect infinite recursion

    ############## """Command related methods""" ###############
    def read_clean(self, ts_file):
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

    def parse(self):
        """
        First parsing for commands except "fin"
        Second parsing for "fin"
        """
        if not self.check_grammar():
            raise Exception(f"Syntax error")
        self.commands = [Command(i, command) for i, command in enumerate(self.commands)]
        # First parsing
        linear = ["I", "P", "D", "G", "1", "0", "(0)", "(1)"]
        command_stack = []
        for i, command in enumerate(self.commands):
            if command.value == "#":
                break  # Commands after # will not be parsed
            elif command.value in linear:
                command.left = self.commands[i + 1]
            elif command.value == "si":
                command_stack.append(command)
                command.left = self.commands[i + 1]
            elif command.value == "boucle":
                command_stack.append(command)
                command.left = self.commands[i + 1]
            elif command.value == "}":
                match = command_stack.pop()
                if match.value == "si":
                    command.left = self.commands[i + 1]
                    match.right = self.commands[i + 1]
                if match.value == "boucle":
                    command.left = match
                    match.right = self.commands[i + 1]
            elif command.value == "fin":
                if not command_stack:
                    command.left = self.commands[-1]
                continue  # Parse in second parsing
            else:
                raise Exception(f"Invalid command: {command}")
        # Second parsing
        command_stack = []
        for i, command in enumerate(self.commands):
            if command.value == "boucle":
                command_stack.append(command)
            if command.value == "fin":
                try:
                    match_boucle = command_stack.pop()
                    command.left = match_boucle.right
                except Exception:
                    continue

    ############## """Tape related methods""" ###############
    def generate_tape(self, *args: int):
        self.tape = ["0", "0"]
        for arg in args:
            self.tape += ["1" for _ in range(arg + 1)] + ["0", "0"]  # Each arg seperated by two "0"
        current_length = len(self.tape)
        if current_length > self.tape_length:
            self.tape = []
            raise Exception(f"Maximum tape length: {self.tape_length}. Buy a better computer (I mean turing machine).")
        else:
            self.tape = self.tape + ["0" for _ in range(self.tape_length - current_length)]

    def show_tape(self):
        print("".join(self.tape) + "\n")

    ############## """Execution""" ###############
    def execute(self):
        if not self.tape:
            raise Exception("Tape is empty")
        if not self.commands:
            raise Exception("Commands empty")
        if not isinstance(self.commands[0], Command):
            self.parse()

        # Execution
        current_command = self.commands[0]
        io_head_index = 2
        step_count = 0

        print("Initial tape:")
        self.show_tape()

        while True:
            # Check for possible stack overflowing
            if step_count > self.allowing_step:
                raise (Exception(f"Exceeding allowing steps: {self.allowing_step}. Check for infinite recursion."))
            if io_head_index >= len(self.tape) or io_head_index < 0:
                print(f"On step {step_count}. Stack overflow. Io-head exceeding tape")
                break
            # Execution
            if current_command.value == "#":
                break
            elif current_command.value == "I":
                print(f"Tape on step {step_count}:")
                self.show_tape()
                current_command = current_command.left
            elif current_command.value == "P":
                input("Press any key + enter to continue...")
                print("Congratulations you didn't press the power key and the computer is still on!")
                current_command = current_command.left
            elif current_command.value == "D":
                io_head_index += 1
                current_command = current_command.left
            elif current_command.value == "G":
                io_head_index -= 1
                current_command = current_command.left
            elif current_command.value == "1":
                self.tape[io_head_index] = "1"
                current_command = current_command.left
            elif current_command.value == "0":
                self.tape[io_head_index] = "0"
                current_command = current_command.left
            elif current_command.value == "si":
                si_value = self.commands[current_command.index + 1].value[1]  # Get x in "(x)"
                if si_value == self.tape[io_head_index]:
                    current_command = current_command.left
                else:
                    current_command = current_command.right
            elif current_command.value in ["(0)", "(1)", "boucle", "fin", "}"]:
                current_command = current_command.left
            else:
                raise Exception(f"Invalid command: {current_command}")
            step_count += 1

        print("Final tape:")
        self.show_tape()
