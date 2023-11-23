"""
Defines classes that represent blocks of C logic.
"""

from utilities import print_stderr, is_tree, is_token, find_minimum_total_bits
import bitfielder_globals

class Attr_Holder:
    """
    Used for holding miscellaneous attributes
    """
    pass

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
    
    def do_math_for_properties(self):
        """
        Fills in missing bits values on property statements. Should be overridden by super property statements and program.
        """
        print_stderr("Error: called do_math_for_properties() on wrong object")
        exit(1)

    def _do_math_for_properties_helper(self, total_bits):
        """
        Helper function for do_math_for_properties().
        """
        # first pass: count number of unknown bits parameters and sum of bits besides unknowns
        if total_bits is None:
            maximum_unknowns = 0
        else:
            maximum_unknowns = 1
        unknowns = 0
        sum_of_bits_besides_unknowns = 0
        for content in self.contents:
            if isinstance(content, (C_Property_Stmt, C_Super_Property)):
                if content.bits is None:
                    unknowns += 1
                else:
                    sum_of_bits_besides_unknowns += content.bits

        if unknowns > maximum_unknowns:
            print_stderr("Error: more unknown bits parameters (%r) than allowed. "
                         "If fixed width int type is unrecognized, 0 unknown bits parameters are allowed." % unknowns)
            exit(1)

        # second pass: fill in unknown bits parameter as necessary, and fill in offset; also fill in prefix lists
        sum_of_bits = 0
        for content in self.contents:
            if isinstance(content, (C_Property_Stmt, C_Super_Property)):
                content.offset = sum_of_bits
                if content.bits is None:
                    content.bits = total_bits - sum_of_bits_besides_unknowns
                    if content.bits < 0:
                        print_stderr("Error 1: some collection of properties added up to too many bits (%r) "
                                     "to fit in minimum total bits (%r)" % (sum_of_bits_besides_unknowns, total_bits))
                        exit(1)
                sum_of_bits += content.bits

                # fill in prefix lists
                content.prefix_list = self.prefix_list + [self.name.name_str]

                # if it's a super property, recursively call do_math_for_properties()
                if isinstance(content, C_Super_Property):
                    content.do_math_for_properties()

                # add to property_dict
                if content.name.name_str in bitfielder_globals.property_dict:
                    print_stderr("Error: defined a property name twice")
                    exit(1)
                else:
                    bitfielder_globals.property_dict[content.name.name_str] = content.bits
        
        if total_bits is not None:
            if sum_of_bits > total_bits:
                print_stderr("Error 2: some collection of properties added up to too many bits (%r) "
                             "to fit in minimum total bits (%r)" % (sum_of_bits, total_bits))
                exit(1)

    def convert_to_code(self):
        """
        Returns a list of C code strings that will be separated by newlines. Should be overridden by some subclasses.
        """
        ret = []
        for content in self.contents:
            if isinstance(content, C_Block):
                ret += content.convert_to_code()
        return ret

class C_Program(C_Block):
    grammar_rule_name = "program"
    fixed_int_name = None
    name = None # Attr_Holder instance that imitates a C_Name instance
    prefix_list = []

    def process_contents(self):
        for content in self.contents:
            if isinstance(content, C_Fixed_Int_Stmt):
                self.fixed_int_name = content.name.name_str
            if isinstance(content, C_Prefix_Stmt):
                name_obj = Attr_Holder()
                name_obj.name_str = content.prefix_string # kluge to imitate C_Name object
                self.name = name_obj
                bitfielder_globals.prefix_name = self.name.name_str

    def do_math_for_properties(self):
        self._do_math_for_properties_helper(bitfielder_globals.minimum_total_bits)

    def convert_to_code(self):
        ret = []
        header_name = self.fixed_int_name.upper() + "_H"

        ret += [""]
        ret += ["#ifndef %s" % header_name]
        ret += ["#define %s" % header_name]
        ret += [""]
        ret += ["#include <cstdint>"]
        ret += [""]

        for content in self.contents:
            if isinstance(content, C_Block):
                ret += content.convert_to_code()
                ret += [""]

        ret += [""]
        ret += [""]
        ret += ["#endif"]

        return ret

class C_Fixed_Int_Stmt(C_Block):
    grammar_rule_name = "fixed_int_stmt"
    c_int_type_string = None
    name = None

    def process_contents(self):
        self.c_int_type_string = self.contents[0]
        self.name = self.contents[1]

        bitfielder_globals.minimum_total_bits = find_minimum_total_bits(self.c_int_type_string)

    def convert_to_code(self):
        return ["typedef %s %s;" % (self.c_int_type_string, self.name.name_str)]

class C_Prefix_Stmt(C_Block):
    grammar_rule_name = "prefix_stmt"
    prefix_string = None

    def process_contents(self):
        self.prefix_string = self.contents[0]

class C_Comment(C_Block):
    grammar_rule_name = "c_comment"
    number = None
    content_string = None

    def process_contents(self):
        self.number = self.contents[0]
        self.content_string = bitfielder_globals.comment_list[self.number]
        print_stderr("comment number: %r, content_string: %r" % (self.number, self.content_string))

    def convert_to_code(self):
        return [self.content_string]

class C_Property_Stmt(C_Block):
    grammar_rule_name = "property_stmt"
    name = None # C_Name instance
    bits = None # integer
    offset = None # integer
    prefix_list = [] # strings

    def process_contents(self):
        self.name = self.contents[0]
        bits_obj = self.contents[1]
        if bits_obj is not None:
            self.bits = bits_obj.bits
        print_stderr("Vars: %r, %r" % (self.name, self.bits))

    def convert_to_code(self):
        ret = []
        ret += ["Property statement %s: bits = %r, inner offset = %r, "
                "prefix list = %r" % (self.name, self.bits, self.offset, self.prefix_list)] ###

        # inner_prefix = self.prefix_list[-1]
        bits = self.bits
        offset = self.offset
        name = self.name.name_str

        for i in range(len(self.prefix_list)):
            current_prefix = self.prefix_list[-1-i]
            if i == 0:
                # accessor
                ret += [f"#define {current_prefix}_{name}(b) ( ((b)>>{offset}) & ((1<<{bits}) - 1) )"]
                # constructor
                ret += [f"#define C_{current_prefix}_{name}(v) ((v) << {offset})"]
            else:
                # accessor
                ret += [f"#define {current_prefix}_{name}(b) {previous_prefix}_{name}({current_prefix}_{previous_prefix}(b))"]
                # constructor
                ret += [f"#define C_{current_prefix}_{name}(v) C_{current_prefix}_{previous_prefix}(C_{previous_prefix}_{name}(v))"]
            previous_prefix = current_prefix
        return ret

class C_Super_Property(C_Block):
    grammar_rule_name = "super_property"
    name = None # C_Name instance
    bits = None # integer
    offset = None # integer
    prefix_list = [] # strings
    codeable_child = None

    def process_contents(self):
        # set information to first child's, save it in a variable, then delete it from contents (first child in grammar represents this object)
        first_child = self.contents[0]
        self.name = first_child.name
        self.bits = first_child.bits
        self.codeable_child = first_child
        del self.contents[0]
        # if we don't know bits, but every child does, set bits to the sum of children's bits
        total_child_bits = 0
        can_calculate_bits = True
        for child_instance in self.contents:
            if child_instance.bits is None:
                can_calculate_bits = False
                break
            total_child_bits += child_instance.bits
        if can_calculate_bits:
            if self.bits is None:
                self.bits = total_child_bits
            elif self.bits < total_child_bits:
                print_stderr("Error: super property %s has explicitly set bits (%r) "
                             "to be too small for its children (sum %r)" % (self.name, self.bits, total_child_bits))
                exit(1)
        # print_stderr("Vars: %r, %r" % (self.name, self.bits))

    def do_math_for_properties(self):
        self._do_math_for_properties_helper(self.bits)

    def convert_to_code(self):
        ret = ["Super property statement %s: bits = %r, inner offset = %r" % (self.name, self.bits, self.offset)] ###
        self.codeable_child.bits = self.bits
        self.codeable_child.offset = self.offset
        self.codeable_child.prefix_list = self.prefix_list
        ret += self.codeable_child.convert_to_code()
        for content in self.contents:
            if isinstance(content, C_Block):
                ret += [""]
                ret += content.convert_to_code()
        ret += [""]
        return ret

# constructors produced automatically by C_Program

class C_Values(C_Block):
    grammar_rule_name = "values_stmt"
    name = None # C_Name instance

    def process_contents(self):
        self.name = self.contents[0]
        del self.contents[0]

        for content in self.contents:
            if isinstance(content, C_Name):
                item_name_str = content.name_str
                bitfielder_globals.constant_names += [item_name_str]

    def convert_to_code(self):
        ret = []

        statement_name_str = self.name.name_str
        if statement_name_str not in bitfielder_globals.property_dict:
            print_stderr("Error: values statement references unknown property %s" % (statement_name_str))
            exit(1)

        i = 1
        for content in self.contents:
            if isinstance(content, C_Name):
                item_name_str = content.name_str
                bits = bitfielder_globals.property_dict[statement_name_str]
                prefix = bitfielder_globals.prefix_name
                ret += [f"#define {item_name_str} ( C_{prefix}_{statement_name_str}({i}) )"]

                allowed_values = pow(2, bits) - 1
                if i > allowed_values:
                    print_stderr("Error: values in value statement exceeded allowed values (%r)" % (allowed_values,))
                    exit(1)

                i += 1

        # ret += [""]

        return ret

class C_Constant_Stmt(C_Block):
    grammar_rule_name = "constant_stmt"
    name = None # C_Name instance

    def process_contents(self):
        self.name = self.contents[0]
        bitfielder_globals.constant_names += [self.name.name_str]

    def convert_to_code(self):
        ret = []
        ret += ["Constant statement %s" % (self.name,)] ###

        name = self.name.name_str
        ret_str = f"#define {name} ( "
        string_list = []
        for content in self.contents:
            if isinstance(content, C_Constant_Expr):
                string_list += [str(content)]
        ret_str += " | ".join(string_list)
        ret_str += " )"

        ret += [ret_str]
        return ret

class C_Constant_Expr(C_Block):
    grammar_rule_name = "constant_expr"
    name = None
    value = None

    def __str__(self):
        name = self.name.name_str
        value = self.value
        prefix = bitfielder_globals.prefix_name
        if value is None:
            ret_str = f"{name}"
        else:
            ret_str = f"C_{prefix}_{name}({value})"
        return ret_str

    def process_contents(self):
        self.name = self.contents[0]

        c_len = len(self.contents)

        # using an existing constant
        for name_str in bitfielder_globals.constant_names:
            if name_str == self.name.name_str:
                if c_len == 2:
                    print_stderr("Error: used existing constant with a value in constant statement")
                    exit(1)
                return

        # using a property constructor
        if c_len == 2:
            self.value = self.contents[1]
        elif c_len == 1:
            # using a boolean property constructor
            self.value = 1
        else:
            print_stderr("Error: unexpected length of contents in constant_expr")
            exit(1)

class C_Name(C_Block):
    grammar_rule_name = "name"
    name_str = None

    def __str__(self):
        return self.name_str

    def process_contents(self):
        assert type(self.contents[0]) == str
        self.name_str = self.contents[0]

class C_Bits(C_Block):
    grammar_rule_name = "bits"
    bits = None

    def process_contents(self):
        assert type(self.contents[0]) == int
        self.bits = self.contents[0]

    
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