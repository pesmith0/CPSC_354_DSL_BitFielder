"""
Compiles lark output into C code.
"""

from c_blocks import C_Program

def compile_to_c(lark_output):
    # lark_output to abstract C blocks
    c_program = C_Program(lark_output)

    # fill in abstract C blocks (including comments), turning them into concrete blocks
    c_program.do_math_for_properties()

    # concrete C blocks to strings of C code
    c_code = c_program.convert_to_code()

    # merge into a single string
    c_code_string = "\n".join(c_code)

    return c_code_string