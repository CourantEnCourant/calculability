# MTdv programming language v0.3

## General
* MTdv compiler is an interpreter/compiler for a French turing-tarpit called "Machine de Turing de del Vigna". It allows compiling and executing scripts written in MTdv
* Examples of programs written in MTdv in `./ts_scripts`
* All Python scripts in `./scripts`
* For how to use Python scripts, use `python [script.py] -h` for help
* All compiled `.py` files in `./exec`

## MTdv language
* Documentation to be written...

## Requirements
* `python 3.10` or above recommended
* No third-party libraries required

## Interpreter
* Example of usage, to calculate `8 * 9`:
  * `python execute.py --tape_length 200 --allowing_step 50000 --script ../ts_scripts/multiplicateur.1.TS --args_turing 8 9`

## Compiler
* Use `python compile.py [ts_script.TS]` to compile a .TS script into `./exec`
* Use `python ./exec/ts_script.py [args]` to execute the compiled script
* Example of usage, to calculate `3 * 5`:
  * `python compile.py ../ts_scripts/multiplicateur.1.TS`
  * `python ../exec/multiplicateur.1.py 3 5`

## Update journal:
* Basically replaced `for` and `while` with recursive functions
* `return` to be replaced on next update