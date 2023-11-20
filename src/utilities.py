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