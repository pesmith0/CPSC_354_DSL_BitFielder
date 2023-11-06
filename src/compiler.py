"""
Compiles lark output into C code.
"""

from c_blocks import C_Program

def compile_to_c(lark_output):
    # lark_output to abstract C blocks
    c_program = C_Program(lark_output)

    # fill in abstract C blocks (including comments), turning them into concrete blocks

    # concrete C blocks to strings of C code

    return str(c_program)