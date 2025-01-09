import sys
args = sys.argv[1:]

tape = ["0", "0"]
for arg in args:
    tape += ["1" for _ in range(int(arg) + 1)] + ["0", "0"]

if len(tape) <= 50:
    tape = tape + ["0" for _ in range(50 - len(tape))]

print(f"Initial tape:")
print("".join(tape))

io_head_index = 2
while True:
    io_head_index += 1
    tape[io_head_index] = "0"
    io_head_index += 1
    if tape[io_head_index] == '0':
        break
print("".join(tape))
io_head_index -= 1
while True:
    io_head_index -= 1
    print("".join(tape))
    while True:
        io_head_index -= 1
        if tape[io_head_index] == '0':
            break
    io_head_index -= 1
    if tape[io_head_index] == '0':
        break
    io_head_index += 1
    tape[io_head_index] = "1"
    while True:
        io_head_index += 1
        if tape[io_head_index] == '0':
            break
    io_head_index -= 1
    tape[io_head_index] = "0"
io_head_index += 1
io_head_index += 1
print("".join(tape))
print(f"Final tape:")
print("".join(tape))
