"""
Defines classes that represent blocks of C logic.
"""

from utilities import print_stderr, is_tree, is_token

class C_Block:
    grammar_rule_name = None # some subclasses will directly correspond to lark tree tokens
    def __init__(self, lark_tree):
        self.lark_tree = lark_tree
        assert is_tree(lark_tree, self.grammar_rule_name)
        self.contents = []
        self.fill_contents()
        self.process_contents()

    def fill_contents(self):
        # tree = self.lark_tree
        # print_stderr("class: ", self.__class__)
        # print_stderr("type: ", type(tree))
        # if is_tree(tree):
        #     print_stderr("data: %r" % tree.data)
        # raise NotImplementedError

        tree = self.lark_tree
        # for every thing in children, check its type and add a corresponding class into contents
        for child in tree.children:
            # print_stderr("child: ", child)
            if is_tree(child):
                block_class = get_class_from_tree(child)
                new_instance = block_class(child)
                self.contents += [new_instance]
            elif is_token(child):
                new_value = convert_value(child)
                print_stderr("child value: %r" % (new_value, ))
                self.contents += [new_value]
            elif child is None:
                self.contents += [child]
            else:
                print_stderr("Error: encountered unknown child in children during fill_contents")
                exit(1)
    
    def process_contents(self):
        """
        Should be overridden on subclasses that need to figure something out about their contents after fill_contents()
        """
        pass

class C_Program(C_Block):
    grammar_rule_name = "program"

class C_Fixed_Int_Stmt(C_Block):
    grammar_rule_name = "fixed_int_stmt"

class C_Prefix_Stmt(C_Block):
    grammar_rule_name = "prefix_stmt"

class C_Comment(C_Block):
    grammar_rule_name = "c_comment"

class C_Property_Stmt(C_Block):
    grammar_rule_name = "property_stmt"
    name = None # C_Name instance
    bits = None # integer

    def process_contents(self):
        self.name = self.contents[0]
        bits_obj = self.contents[1]
        if bits_obj is not None:
            self.bits = bits_obj.bits
        print_stderr("Vars: %r, %r" % (self.name, self.bits))

class C_Super_Property(C_Property_Stmt):
    grammar_rule_name = "super_property"

# constructors produced automatically by C_Program

class C_Values(C_Block):
    grammar_rule_name = "values_stmt"

class C_Constant_Stmt(C_Block):
    grammar_rule_name = "constant_stmt"

class C_Name(C_Block):
    grammar_rule_name = "name"

class C_Bits(C_Block):
    grammar_rule_name = "bits"
    bits = None

    def process_contents(self):
        assert type(self.contents[0]) == int
        self.bits = self.contents[0]

class C_Constant_Expr(C_Block):
    grammar_rule_name = "constant_expr"

    
def get_class_from_tree(lark_tree):
    assert is_tree(lark_tree), "get_class_from_tree assertion failed with lark_tree = %r" % ((lark_tree, type(lark_tree)), )
    
    if lark_tree.data == C_Fixed_Int_Stmt.grammar_rule_name:
        return C_Fixed_Int_Stmt
    elif lark_tree.data == C_Prefix_Stmt.grammar_rule_name:
        return C_Prefix_Stmt
    elif lark_tree.data == C_Comment.grammar_rule_name:
        return C_Comment
    elif lark_tree.data == C_Property_Stmt.grammar_rule_name:
        return C_Property_Stmt
    elif lark_tree.data == C_Super_Property.grammar_rule_name:
        return C_Super_Property
    elif lark_tree.data == C_Values.grammar_rule_name:
        return C_Values
    elif lark_tree.data == C_Constant_Stmt.grammar_rule_name:
        return C_Constant_Stmt
    elif lark_tree.data == C_Name.grammar_rule_name:
        return C_Name
    elif lark_tree.data == C_Bits.grammar_rule_name:
        return C_Bits
    elif lark_tree.data == C_Constant_Expr.grammar_rule_name:
        return C_Constant_Expr
    else:
        print_stderr("Error: called get_class_from_tree with unknown tree type: %r" % (lark_tree.data,))
        exit(1)

def convert_value(lark_token):
    new_value = lark_token.value
    typ = lark_token.type
    if typ == "INTEGER":
        new_value = int(new_value)
    # else:
    #     print_stderr("Error: called convert_value with unknown token type: %r" % (typ,))
    #     exit(1)
    return new_value