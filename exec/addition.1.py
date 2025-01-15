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


in_loop_1 = True
in_loop_2 = True
in_loop_3 = True
in_loop_4 = True
in_loop_5 = True
in_loop_6 = True

print(f"Initial tape:")
show_tape()

show_tape()
def loop_1():
    global in_loop_1, tape, io_head_index
    if in_loop_1:
        if tape[io_head_index] == '0':
            return None
        io_head_index += 1
        loop_1()
loop_1()
def loop_2():
    global in_loop_2, tape, io_head_index
    if in_loop_2:
        def loop_3():
            global in_loop_3, tape, io_head_index
            if in_loop_3:
                io_head_index += 1
                if tape[io_head_index] == '1':
                    return None
                loop_3()
        loop_3()
        tape[io_head_index] = "0"
        io_head_index += 1
        if tape[io_head_index] == '0':
            return None
        def loop_4():
            global in_loop_4, tape, io_head_index
            if in_loop_4:
                io_head_index -= 1
                if tape[io_head_index] == '1':
                    return None
                loop_4()
        loop_4()
        io_head_index += 1
        tape[io_head_index] = "1"
        io_head_index += 1
        loop_2()
loop_2()
def loop_5():
    global in_loop_5, tape, io_head_index
    if in_loop_5:
        io_head_index -= 1
        if tape[io_head_index] == '1':
            return None
        loop_5()
loop_5()
def loop_6():
    global in_loop_6, tape, io_head_index
    if in_loop_6:
        io_head_index -= 1
        if tape[io_head_index] == '0':
            return None
        loop_6()
loop_6()
io_head_index += 1
show_tape()
print(f"Final tape:")
show_tape()
