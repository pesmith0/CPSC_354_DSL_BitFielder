# CPSC_354 Class Project: "BitFielder" Domain-Specific Language

Group Members: Peter Smith

This project is a DSL intended to streamline the process of implementing memory-efficient integer ID systems in C++ by way of bit fields, e.g. a unique integer ID for every block in Minecraft that also contains various properties of the block, such as hardness and flammability. The motivation is that directly implementing them in C++ is tedious and prone to typos or mistakes.

A Python program will parse the BitFielder input and compile it to C++. This DSL is not interpreted.

===

The program is located in /src. Python 3 is required. To run it:

```py bitfielder_parser.py <input filename>```

This will print a tree of tokens as output in both normal and pretty formats.

In /docs there are two example input files, as well as a guide to the grammar syntax "grammar.txt" and a list of references "annotated-references.md".

===

The current roadmap is to implement the feature of compiling the tree to C, and possibly more grammar features.