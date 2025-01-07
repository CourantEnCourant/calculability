""""""
from turing_machine import TuringMachine, Command

import logging
from pathlib import Path
from typing import Sequence, Optional


def main(tape_length: int, allowing_step: int, script: Path, args_turing: list[int]):
    # Logging
    logging.basicConfig(level=logging.INFO)
    logging.info(f".TS script: {script}")
    logging.info(f"Arguments on tape: {args_turing}\n")
    # Turing machine configuration
    turing = TuringMachine(tape_length, allowing_step)
    turing.read_clean(script)
    turing.generate_tape(*args_turing)
    # Execution
    turing.parse()
    turing.execute()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Execute a TS script")
    parser.add_argument("-tl", "--tape_length",
                        default=80,
                        type=int,
                        metavar="",
                        help="Tape length. Default set to 80")
    parser.add_argument("-as", "--allowing_step",
                        default=9999,
                        type=int,
                        metavar="",
                        help="Maximum allowing steps for the Turing Machine. Default set to 9999")
    parser.add_argument("-s", "--script",
                        default=Path("../ts_scripts/addition.1.TS"),
                        type=Path,
                        metavar="",
                        help="TS script to parse. Default set to addition script")
    parser.add_argument("-a", "--args_turing",
                        default=[5, 8],
                        type=int,
                        nargs="*",
                        metavar="",
                        help="Argument(s) passed to Turing Machine, shown on initial tape. Default set to [5, 8], for addition")
    args = parser.parse_args()

    main(tape_length=args.tape_length,
         allowing_step=args.allowing_step,
         script=args.script,
         args_turing=args.args_turing)
