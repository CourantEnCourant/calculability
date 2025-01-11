import sys
args = sys.argv[1:]

tape = ["0", "0"]
for arg in args:
    tape += ["1" for _ in range(int(arg) + 1)] + ["0", "0"]

if len(tape) <= 50:
    tape = tape + ["0" for _ in range(50 - len(tape))]

io_head_index = 2
show_tape_index = 0


def show_tape():
    global tape, show_tape_index
    if show_tape_index < len(tape):
        print(tape[show_tape_index], end="")
        show_tape_index += 1
        show_tape()
    else:
        print("")
        show_tape_index = 0


print(f"Initial tape:")
show_tape()

show_tape()
def loop_1(tape, io_head_index):
    if tape[io_head_index] == '0':
        return tape, io_head_index
    io_head_index += 1
    return loop_1(tape, io_head_index)
tape, io_head_index = loop_1(tape, io_head_index)
def loop_2(tape, io_head_index):
    io_head_index += 1
    if tape[io_head_index] == '1':
        return tape, io_head_index
    return loop_2(tape, io_head_index)
tape, io_head_index = loop_2(tape, io_head_index)
def loop_3(tape, io_head_index):
    io_head_index += 1
    if tape[io_head_index] == '0':
        return tape, io_head_index
    return loop_3(tape, io_head_index)
tape, io_head_index = loop_3(tape, io_head_index)
io_head_index += 1
tape[io_head_index] = "1"
io_head_index -= 1
def loop_4(tape, io_head_index):
    io_head_index -= 1
    if tape[io_head_index] == '0':
        return tape, io_head_index
    return loop_4(tape, io_head_index)
tape, io_head_index = loop_4(tape, io_head_index)
def loop_5(tape, io_head_index):
    io_head_index -= 1
    if tape[io_head_index] == '1':
        return tape, io_head_index
    return loop_5(tape, io_head_index)
tape, io_head_index = loop_5(tape, io_head_index)
def loop_6(tape, io_head_index):
    tape[io_head_index] = "0"
    io_head_index -= 1
    if tape[io_head_index] == '0':
        return tape, io_head_index
    io_head_index += 1
    def loop_7(tape, io_head_index):
        io_head_index += 1
        if tape[io_head_index] == '1':
            return tape, io_head_index
        return loop_7(tape, io_head_index)
    tape, io_head_index = loop_7(tape, io_head_index)
    def loop_8(tape, io_head_index):
        io_head_index += 1
        if tape[io_head_index] == '0':
            return tape, io_head_index
        return loop_8(tape, io_head_index)
    tape, io_head_index = loop_8(tape, io_head_index)
    io_head_index -= 1
    def loop_9(tape, io_head_index):
        tape[io_head_index] = "0"
        io_head_index -= 1
        if tape[io_head_index] == '0':
            return tape, io_head_index
        io_head_index += 1
        def loop_10(tape, io_head_index):
            io_head_index += 1
            if tape[io_head_index] == '1':
                return tape, io_head_index
            return loop_10(tape, io_head_index)
        tape, io_head_index = loop_10(tape, io_head_index)
        def loop_11(tape, io_head_index):
            io_head_index += 1
            if tape[io_head_index] == '0':
                return tape, io_head_index
            return loop_11(tape, io_head_index)
        tape, io_head_index = loop_11(tape, io_head_index)
        tape[io_head_index] = "1"
        def loop_12(tape, io_head_index):
            io_head_index -= 1
            if tape[io_head_index] == '0':
                return tape, io_head_index
            return loop_12(tape, io_head_index)
        tape, io_head_index = loop_12(tape, io_head_index)
        def loop_13(tape, io_head_index):
            io_head_index -= 1
            if tape[io_head_index] == '1':
                return tape, io_head_index
            return loop_13(tape, io_head_index)
        tape, io_head_index = loop_13(tape, io_head_index)
        return loop_9(tape, io_head_index)
    tape, io_head_index = loop_9(tape, io_head_index)
    io_head_index += 1
    tape[io_head_index] = "1"
    def loop_14(tape, io_head_index):
        io_head_index += 1
        if tape[io_head_index] == '1':
            return tape, io_head_index
        return loop_14(tape, io_head_index)
    tape, io_head_index = loop_14(tape, io_head_index)
    io_head_index -= 1
    def loop_15(tape, io_head_index):
        io_head_index -= 1
        if tape[io_head_index] == '1':
            return tape, io_head_index
        tape[io_head_index] = "1"
        return loop_15(tape, io_head_index)
    tape, io_head_index = loop_15(tape, io_head_index)
    def loop_16(tape, io_head_index):
        io_head_index -= 1
        if tape[io_head_index] == '1':
            return tape, io_head_index
        return loop_16(tape, io_head_index)
    tape, io_head_index = loop_16(tape, io_head_index)
    return loop_6(tape, io_head_index)
tape, io_head_index = loop_6(tape, io_head_index)
def loop_17(tape, io_head_index):
    io_head_index += 1
    if tape[io_head_index] == '1':
        return tape, io_head_index
    return loop_17(tape, io_head_index)
tape, io_head_index = loop_17(tape, io_head_index)
def loop_18(tape, io_head_index):
    tape[io_head_index] = "0"
    io_head_index += 1
    if tape[io_head_index] == '0':
        return tape, io_head_index
    return loop_18(tape, io_head_index)
tape, io_head_index = loop_18(tape, io_head_index)
io_head_index += 1
show_tape()
print(f"Final tape:")
show_tape()
