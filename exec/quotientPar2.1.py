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

print(f"Initial tape:")
show_tape()

def loop_1():
    global in_loop_1, tape, io_head_index
    if in_loop_1:
        io_head_index += 1
        tape[io_head_index] = "0"
        io_head_index += 1
        if tape[io_head_index] == '0':
            in_loop_1 = False
        else:
            loop_1()
    in_loop_1 = True
loop_1()
show_tape()
io_head_index -= 1
def loop_2():
    global in_loop_2, tape, io_head_index
    if in_loop_2:
        io_head_index -= 1
        show_tape()
        def loop_3():
            global in_loop_3, tape, io_head_index
            if in_loop_3:
                io_head_index -= 1
                if tape[io_head_index] == '0':
                    in_loop_3 = False
                else:
                    loop_3()
            in_loop_3 = True
        loop_3()
        io_head_index -= 1
        if tape[io_head_index] == '0':
            in_loop_2 = False
        else:
            io_head_index += 1
            tape[io_head_index] = "1"
            def loop_4():
                global in_loop_4, tape, io_head_index
                if in_loop_4:
                    io_head_index += 1
                    if tape[io_head_index] == '0':
                        in_loop_4 = False
                    else:
                        loop_4()
                in_loop_4 = True
            loop_4()
            io_head_index -= 1
            tape[io_head_index] = "0"
            loop_2()
    in_loop_2 = True
loop_2()
io_head_index += 1
io_head_index += 1
show_tape()
print(f"Final tape:")
show_tape()
