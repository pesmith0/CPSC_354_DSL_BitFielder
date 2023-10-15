To use the prototype, Python 3 is required.

In the same directory as bitfielder_parser.py, create a text file to use as input, according to the grammar rules below.

To run the code:
```py bitfielder_parser.py <input filename>```

This will print a tree of tokens as output.

Grammar rules:

```
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
