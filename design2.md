This is a python program that demonstrates how [Lark](https://github.com/lark-parser/lark) can be used to parse BitFielder.
Not all of the BitFielder syntax is added yet.

```
from lark import Lark
json_parser = Lark(r"""
    program : fixed_int_stmt [prefix_stmt] stmt*
                   
    fixed_int_stmt : ESCAPED_STRING name
    
    name : ESCAPED_STRING
                   
    prefix_stmt : "prefix" ESCAPED_STRING
    
    stmt : property_stmt
    
    property_stmt : "property" name bits
    bits : SIGNED_NUMBER
                   
    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS

    """, start='program')

text = '"uint_fast32_t" "BlockID"    prefix "BLOCK_"    property "HEALTH" 3'
print( json_parser.parse(text).pretty() )
