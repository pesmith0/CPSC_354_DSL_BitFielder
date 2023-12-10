"""
Utilities for bitfielder
"""

import sys
import lark

def print_stderr(*message):
    print(*message, file=sys.stderr)

def is_tree(obj, tree_type = None):
    if tree_type == None:
        return type(obj) == lark.tree.Tree
    else:
        assert type(tree_type) == str
        # obj.data is a lark Token which inherits from str, so == works
        return (type(obj) == lark.tree.Tree) and (obj.data == tree_type)
    
def is_token(obj):
    return type(obj) == lark.lexer.Token

def find_minimum_total_bits(c_int_type_string):
    """
    Uses this list of C fixed width integer types: https://en.cppreference.com/w/c/types/integer
    """
    if c_int_type_string.endswith("t8_t"):
        return 8
    elif c_int_type_string.endswith("t16_t"):
        return 16
    elif c_int_type_string.endswith("t32_t"):
        return 32
    elif c_int_type_string.endswith("t64_t"):
        return 64
    else:
        return None