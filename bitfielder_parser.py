from tokenize import tokenize, INDENT, DEDENT, NEWLINE, ENCODING
from io import BytesIO
from lark import Lark

def tokenize_bitfielder(s):
    """
    Takes a string. Replaces certain tokens with ones that Lark can parse. Returns the modified string.
    """
    result = []
    g = tokenize(BytesIO(s.encode('utf-8')).readline)  # tokenize the string
    for token_type, token_value, _begin_pos, _end_pos, _line_content in g:
        if token_type == INDENT:
            result.append("{{{")
        elif token_type == DEDENT:
            result.append("}}}")
        elif token_type == NEWLINE: # there is a separate token for solitary newlines called "NL"
            result.append(";\n")
        elif token_type == ENCODING:
            pass
        else:
            result.append(token_value)
        
    return " ".join(result)

lark_parser = Lark(r"""
    program : fixed_int_stmt [prefix_stmt] stmt*
                   
    IDENTIFIER : /[A-Za-z_][A-Za-z_0-9]*/
                   
    fixed_int_stmt : IDENTIFIER name NL
    
    name : IDENTIFIER
                   
    NL : ";"
                   
    prefix_stmt : "prefix" IDENTIFIER NL
    
    stmt : property_stmt | super_property | values_stmt | constant_stmt
    
    property_stmt : "property" name bits NL
    bits : SIGNED_NUMBER
                   
    super_property : "property" name", prefix" name NL "{{{" property_list
    property_list : property_stmt property_list | property_stmt "}}}"
    
    values_stmt : "values" name ":" NL "{{{" values_list
                   
    values_list : name NL values_list | name NL "}}}"
                   
    constant_stmt : "constant" name "{" expr_list "}" NL
                   
    expr_list : constant_expr "," expr_list | constant_expr
                   
    constant_expr : name | name "(" SIGNED_NUMBER ")"
                   
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS

    """, start='program')


if __name__ == '__main__':
    import sys

    filename = sys.argv[1]
    f = open(filename, "r")
    s = f.read()

    modded_string = tokenize_bitfielder(s)
    
    print("modded_string:\n%r" % modded_string)

    lark_output = lark_parser.parse(modded_string)

    print("%r" % lark_output)

    print("\npretty:")

    print(lark_output.pretty())
