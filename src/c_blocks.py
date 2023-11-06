"""
Defines classes that represent blocks of C logic.
"""

from utilities import print_stderr, is_tree

class C_Block:
    grammar_rule_name = None # some subclasses will directly correspond to lark tree tokens
    def __init__(self, lark_tree):
        self.lark_tree = lark_tree
        assert is_tree(lark_tree, self.grammar_rule_name)
        self.contents = []
        self.fill_contents()

    def fill_contents(self):
        tree = self.lark_tree
        print_stderr("type: ", type(tree))
        if is_tree(tree):
            print_stderr("data: %r" % tree.data)
        raise NotImplementedError

class C_Program(C_Block):
    grammar_rule_name = "program"
    # def fill_contents(self):
    #     pass


class C_Fixed_Int_Stmt(C_Block):
    pass

class C_Prefix_Stmt(C_Block):
    pass

class C_Comment(C_Block):
    pass

class C_Property_Stmt(C_Block):
    pass

class C_Super_Property(C_Block):
    pass

# constructors produced automatically by C_Program

class C_Values(C_Block):
    pass

class C_Constant_Stmt(C_Block):
    pass