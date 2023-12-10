# CPSC_354 Class Project: "BitFielder" Domain-Specific Language

## Group Members
Peter Smith

## Motivation and functionality

This project is a DSL intended to streamline the process of implementing memory-efficient integer ID systems in C++ by way of bit fields, e.g. a unique integer ID for every block in Minecraft that also contains various properties of the block, such as hardness and flammability. The motivation is that directly implementing them in C++ is tedious and prone to typos or mistakes.

A Python program will parse the BitFielder input and compile it to C++. This DSL is not interpreted.

## Installation and running

The program is located in /src. Python 3 and Lark are required. To install Lark:

```pip3 install lark```

To run BitFielder with an example input file:

```python3 src/bitfielder_parser.py docs/example_1.txt```

This will print a tree of tokens as output in both normal and pretty formats. It will by default print the output to the console, but to use the output in a C/C++ project, it should be directed to an output file with an arrow, for example:

```python3 src/bitfielder_parser.py docs/example_1.txt > example_output.h```

In /docs there are two example input files, as well as a guide to the grammar syntax "grammar.txt" and a list of references "annotated-references.md".

The outputted header will work with C++ source files, but a simple change will make it work with a C source file instead: replace ```#include <cstdint>``` with ```#include <inttypes.h>```.

## Explanatory videos and how to extend the project with new features

Here are some videos explaining the general purpose of the project, how to install and run it, and an introduction on how one would extend the project with new features:

[General Info](https://www.youtube.com/watch?v=ilN_uKj5AQ8)

[Technical Introduction](https://www.youtube.com/watch?v=fQhYfLYupiY)

## Future work

In the future some good features to add would be:
* make it so that there can be any number of layers of super properties, such as a super property containing a super property containing a super property etc.
* add support for generating property modifier macros.