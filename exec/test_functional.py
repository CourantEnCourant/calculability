from functools import partial
from typing import Callable


def compose(*functions: Callable) -> Callable:
    def composed(*args):
        for func in functions:
            result = func(*args)
            if result == "break":  # 检测终止信号
                return "break"
            args = result  # 更新参数
        return args  # 返回最终结果
    return composed

def show(io_head_index, tape, i=0):
    if i == len(tape):
        print("")  # Just for a \n
        return io_head_index, tape
    print(tape[i], end="")
    return show(io_head_index, tape, i+1)

def right(io_head_index, tape):
    return io_head_index + 1, tape

def left(io_head_index, tape):
    return io_head_index - 1, tape

def one(io_head_index, tape):
    return io_head_index, tape[:io_head_index] + ["1"] + tape[io_head_index + 1:]

def zero(io_head_index, tape):
    return io_head_index, tape[:io_head_index] + ["0"] + tape[io_head_index + 1:]


def if_0(func: Callable) -> Callable:
    def wrapper(io_head_index, tape, *args):
        if tape[io_head_index] == "0":  # 当前位置为 '0'
            return func(io_head_index, tape, *args)  # 执行传入的函数
        return io_head_index, tape, *args  # 否则返回原参数
    return wrapper

def if_1(func: Callable) -> Callable:
    def wrapper(io_head_index, tape, *args):
        if tape[io_head_index] == "1":  # 当前位置为 '0'
            return func(io_head_index, tape, *args)  # 执行传入的函数
        return io_head_index, tape, *args  # 否则返回原参数
    return wrapper


def loop(func: Callable) -> Callable:
    def inner(*args):
        while True:
            result = func(*args)
            if result == "break":  # 检测终止信号
                return args  # 返回输入参数，表示循环结束
            args = result  # 更新参数
    return inner


def end_loop(*args):
    """Return a safeword force end of loop"""
    return "break"