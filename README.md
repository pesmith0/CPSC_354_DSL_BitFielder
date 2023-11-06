# CPSC_354 Class Project: "BitFielder" Domain-Specific Language

Group Members: Peter Smith

This project is a DSL intended to streamline the process of implementing memory-efficient integer ID systems in C++ by way of bit fields, e.g. given properties and information about a Minecraft block, such as hardness and flammability, those properties are turned into integer values and the DSL creates a unique integer ID using those values, since no two blocks have all the same properties. The motivation is that directly implementing them in C++ is tedious and prone to typos or mistakes.

A Python program will parse the BitFielder input and compile it to C++. This DSL is not interpreted.

===

The program is located in /src. Python 3 and Lark are required. To install Lark:

```pip3 install lark```

To run BitFielder:

```python3 bitfielder_parser.py <input filename>```

This will print a tree of tokens as output in both normal and pretty formats.

In /docs there are two example input files, as well as a guide to the grammar syntax "grammar.txt" and a list of references "annotated-references.md".

===

The current roadmap is to implement the feature of compiling the tree to C, and possibly more grammar features.
