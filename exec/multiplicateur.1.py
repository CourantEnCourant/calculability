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
in_loop_7 = True
in_loop_8 = True
in_loop_9 = True
in_loop_10 = True
in_loop_11 = True
in_loop_12 = True
in_loop_13 = True
in_loop_14 = True
in_loop_15 = True
in_loop_16 = True
in_loop_17 = True
in_loop_18 = True

print(f"Initial tape:")
show_tape()

show_tape()
def loop_1():
    global in_loop_1, tape, io_head_index
    if in_loop_1:
        if tape[io_head_index] == '0':
            in_loop_1 = False
        else:
            io_head_index += 1
            loop_1()
    in_loop_1 = True
loop_1()
def loop_2():
    global in_loop_2, tape, io_head_index
    if in_loop_2:
        io_head_index += 1
        if tape[io_head_index] == '1':
            in_loop_2 = False
        else:
            loop_2()
    in_loop_2 = True
loop_2()
def loop_3():
    global in_loop_3, tape, io_head_index
    if in_loop_3:
        io_head_index += 1
        if tape[io_head_index] == '0':
            in_loop_3 = False
        else:
            loop_3()
    in_loop_3 = True
loop_3()
io_head_index += 1
tape[io_head_index] = "1"
io_head_index -= 1
def loop_4():
    global in_loop_4, tape, io_head_index
    if in_loop_4:
        io_head_index -= 1
        if tape[io_head_index] == '0':
            in_loop_4 = False
        else:
            loop_4()
    in_loop_4 = True
loop_4()
def loop_5():
    global in_loop_5, tape, io_head_index
    if in_loop_5:
        io_head_index -= 1
        if tape[io_head_index] == '1':
            in_loop_5 = False
        else:
            loop_5()
    in_loop_5 = True
loop_5()
def loop_6():
    global in_loop_6, tape, io_head_index
    if in_loop_6:
        tape[io_head_index] = "0"
        io_head_index -= 1
        if tape[io_head_index] == '0':
            in_loop_6 = False
        else:
            io_head_index += 1
            def loop_7():
                global in_loop_7, tape, io_head_index
                if in_loop_7:
                    io_head_index += 1
                    if tape[io_head_index] == '1':
                        in_loop_7 = False
                    else:
                        loop_7()
                in_loop_7 = True
            loop_7()
            def loop_8():
                global in_loop_8, tape, io_head_index
                if in_loop_8:
                    io_head_index += 1
                    if tape[io_head_index] == '0':
                        in_loop_8 = False
                    else:
                        loop_8()
                in_loop_8 = True
            loop_8()
            io_head_index -= 1
            def loop_9():
                global in_loop_9, tape, io_head_index
                if in_loop_9:
                    tape[io_head_index] = "0"
                    io_head_index -= 1
                    if tape[io_head_index] == '0':
                        in_loop_9 = False
                    else:
                        io_head_index += 1
                        def loop_10():
                            global in_loop_10, tape, io_head_index
                            if in_loop_10:
                                io_head_index += 1
                                if tape[io_head_index] == '1':
                                    in_loop_10 = False
                                else:
                                    loop_10()
                            in_loop_10 = True
                        loop_10()
                        def loop_11():
                            global in_loop_11, tape, io_head_index
                            if in_loop_11:
                                io_head_index += 1
                                if tape[io_head_index] == '0':
                                    in_loop_11 = False
                                else:
                                    loop_11()
                            in_loop_11 = True
                        loop_11()
                        tape[io_head_index] = "1"
                        def loop_12():
                            global in_loop_12, tape, io_head_index
                            if in_loop_12:
                                io_head_index -= 1
                                if tape[io_head_index] == '0':
                                    in_loop_12 = False
                                else:
                                    loop_12()
                            in_loop_12 = True
                        loop_12()
                        def loop_13():
                            global in_loop_13, tape, io_head_index
                            if in_loop_13:
                                io_head_index -= 1
                                if tape[io_head_index] == '1':
                                    in_loop_13 = False
                                else:
                                    loop_13()
                            in_loop_13 = True
                        loop_13()
                        loop_9()
                in_loop_9 = True
            loop_9()
            io_head_index += 1
            tape[io_head_index] = "1"
            def loop_14():
                global in_loop_14, tape, io_head_index
                if in_loop_14:
                    io_head_index += 1
                    if tape[io_head_index] == '1':
                        in_loop_14 = False
                    else:
                        loop_14()
                in_loop_14 = True
            loop_14()
            io_head_index -= 1
            def loop_15():
                global in_loop_15, tape, io_head_index
                if in_loop_15:
                    io_head_index -= 1
                    if tape[io_head_index] == '1':
                        in_loop_15 = False
                    else:
                        tape[io_head_index] = "1"
                        loop_15()
                in_loop_15 = True
            loop_15()
            def loop_16():
                global in_loop_16, tape, io_head_index
                if in_loop_16:
                    io_head_index -= 1
                    if tape[io_head_index] == '1':
                        in_loop_16 = False
                    else:
                        loop_16()
                in_loop_16 = True
            loop_16()
            loop_6()
    in_loop_6 = True
loop_6()
def loop_17():
    global in_loop_17, tape, io_head_index
    if in_loop_17:
        io_head_index += 1
        if tape[io_head_index] == '1':
            in_loop_17 = False
        else:
            loop_17()
    in_loop_17 = True
loop_17()
def loop_18():
    global in_loop_18, tape, io_head_index
    if in_loop_18:
        tape[io_head_index] = "0"
        io_head_index += 1
        if tape[io_head_index] == '0':
            in_loop_18 = False
        else:
            loop_18()
    in_loop_18 = True
loop_18()
io_head_index += 1
show_tape()
print(f"Final tape:")
show_tape()
