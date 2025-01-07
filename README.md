# MTdv compiler v0.1

## General
* MTdv compiler is a interpreter for a French esoteric programming language called "Machine de Turing de del Vigna". It allows executing scripts written in MTdv
* Examples of programs written in this language in `./ts_scripts`
* Interpreter written in Python in `./scripts`

## MTdv language
* Documentation to be written...

## Requirements
* `python 3.10` or above recommended
* No third-party libraries required

## Usage
* Use `python script/execute.py -h` for detailed documentation
* Default value provided for all options
* An example of advanced usage, to calculate `8 * 9`:
  * `python execute.py --tape_length 200 --allowing_step 50000 --script ../ts_scripts/multiplicateur.1.TS --args_turing 8 9`
