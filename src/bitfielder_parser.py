from tokenize import tokenize, INDENT, DEDENT, NEWLINE, ENCODING, COMMENT
from io import BytesIO
from lark import Lark
import sys
from compiler import compile_to_c
from utilities import print_stderr

def extract_c_comments(s, comment_list):
    """
    Takes a string. Replaces any lines starting with "//" with "comment n" where n is an incrementing number.
    Saves each comment in the comment list.
    """

    lines = s.split("\n")
    # lines = [process_line(line, comment_list) for line in lines]
    lines = map(lambda line: process_line(line, comment_list), lines)

    return "\n".join(lines)

def process_line(line, comment_list):
    if line.strip().startswith("//"):
        comment_list += [line]
        return "c_comment %d" % (len(comment_list) - 1)
    else:
        return line

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
        elif token_type == COMMENT:
            pass
        else:
            result.append(token_value)
        
    return " ".join(result)

# comments are allowed at the start mysteriously

lark_parser = Lark(r"""
    program : c_comment* fixed_int_stmt c_comment* [prefix_stmt] stmt*
                   
    IDENTIFIER : /[A-Za-z_][A-Za-z_0-9]*/
                   
    INTEGER : /[0-9]+/
                   
    fixed_int_stmt : IDENTIFIER name NL
    
    name : IDENTIFIER
                   
    NL : ";"
                   
    prefix_stmt : "prefix" IDENTIFIER NL
    
    stmt : property_stmt | super_property | values_stmt | constant_stmt | NL | c_comment
    
    property_stmt : "property" name [bits] NL
    bits : INTEGER
                   
    super_property : "property" name [bits] "," "prefix" name NL "{{{" property_list
    property_list : property_stmt property_list | property_stmt "}}}"
    
    values_stmt : "values" name ":" NL "{{{" values_list
                   
    values_list : name NL values_list | name NL "}}}"
                   
    constant_stmt : "constant" name "{" expr_list "}" NL
                   
    expr_list : constant_expr "," expr_list | constant_expr
                   
    constant_expr : name | name "(" INTEGER ")"
                   
    c_comment : "c_comment" INTEGER NL
                   
    %import common.WS
    %ignore WS

    """, start='program')

if __name__ == '__main__':
    import sys

    # read from input file
    filename = sys.argv[1]
    f = open(filename, "r")
    s = f.read()
    f.close()

    # extract c comments
    comment_list = []
    s = extract_c_comments(s, comment_list)

    # get lark output
    modded_string = tokenize_bitfielder(s)

    lark_output = lark_parser.parse(modded_string)

    print_stderr("non-pretty:")
    print_stderr("%r" % lark_output)

    print_stderr("\npretty:")
    print_stderr(lark_output.pretty())

    # get c output
    c_output = compile_to_c(lark_output)

    print(c_output)