This file contains a preliminary concept of the planned syntax for the BitFielder DSL.

Context-free grammar syntax (unfinished):
```
<program>       -> <1st stmt>
                 | <1st stmt> \n <2nd stmt>
                 | <1st stmt> \n <2nd stmt> \n <any>
                 | <1st stmt> \n <any>

<any>           -> <prop. stmt> | <super prop.> | values <name>: \n [indent] <values list> | constant <name> { <exp. list> }

# int type is a fixed width integer type
# will support much more fixed width integer types from C, not just three
<1st stmt>      -> <int type> <name>
<int type>      -> uint_fast32_t | uint_least32_t | uint_least64_t
<name>          -> same strings that are allowed for variable names in C

<2nd stmt>      -> prefix <name>

# prop. = property
<prop. stmt>    -> property <name> <bits>
<bits>          -> any positive integer

<super prop.>   -> property <name>, prefix <name> \n [indent] <prop. list>
<prop. list>    -> <prop. stmt> \n <prop. list>
                 | <prop. stmt> \n [dedent]

<values list>   -> <name> \n <values list>
                 | <name> \n [dedent]

# con. exp. = constant expression
# exp. list = constant expression list
<con. exp.>     -> <name>
                 | <name>(<integer>)
<exp. list>     -> <con. exp.>, <exp. list>
                 | <con. exp.>

```
Example input file:
```
# Hashtags indicate a comment, which will be ignored.
// Double slashes indicate text that will be included in the output as a C++ comment. They have to be on their own line.

# At the start we define what type of integer to use for the ID. This line will turn into "typedef uint_fast32_t BlockID;" in C++.
uint_fast32_t BlockID

# We also define a prefix that will go before every property name in C++. For example, a property "HEALTH" would result in a macro "BLOCK_HEALTH" in C++.
prefix BLOCK_

# === Properties ===
# Here we will specify all of the properties we want our ID to contain. These lines will turn into accessor and constructor macros for the properties.
# The syntax is "property <name> <number of bits>"
property HEALTH 3
// Blocks face north by default
property ORIENTATION 2
property OCCUPYING_HEIGHT 4

# Indentation indicates a sub-property, which will use some of the bits that represent its super-property. The super-property can still be accessed as a unit elsewhere in your code.
# Super-properties can optionally specify their own prefix, which will create alternate macros using that prefix which can be used to access properties in the scope of the super-property instead of the entire integer ID like normal.
# For example, the following syntax will define both BLOCK_IS_AIR(b) and SHAPE_IS_AIR(s), where b is the entire BlockID and s is the SHAPE value.
property MATERIAL 7
property SHAPE 9, prefix SHAPE_
    property HEIGHT 4
    property IS_AIR 1
    property IS_WALL 1
    property FALL_THROUGH 1

    # The final sub-property has bits unspecified, meaning it will take up the remaining bits in the super-property. 9 - 4 - 1 - 1 - 1 = 2.
    # Alternatively, we could specify OTHER_SHAPE_BITS and leave SHAPE unspecified. The DSL would calculate the SHAPE bits by summing the sub-properties.
    property OTHER_SHAPE_BITS

# These properties use 25 bits in all. If they exceeded 32 bits, the program would throw an error because we defined the ID as being int32 at the start.

# === Constants ===
# The above code has automatically created accessors and constructors for each property.
# We now want to manually create constants out of those constructors, such as for meaningful IDs that we will use elsewhere in our codebase.
# The syntax is: "constant <name> { <property>(<value>), ... }
# Note: Unmentioned properties will remain at zero, which is their default value.

constant _B_SOLID { IS_WALL, HEIGHT(12) } # We can just say IS_WALL without the (1) because it's a 1-bit property.
constant B_AIR { IS_AIR, FALL_THROUGH }

# For properties for which the value itself is arbitrary, such as the material, we can specify some names for constants and the DSL will assign them values automatically.
# In this case, MAT_GRASS will be a stand-in for MATERIAL(1), MAT_WOOD for MATERIAL(2), etc. The default value MATERIAL(0) is skipped, since 0 is reserved for the default value.
values MATERIAL:
    MAT_GRASS
    MAT_WOOD
    MAT_METAL

constant B_GRASS { MAT_GRASS, _B_SOLID } # In this case MAT_GRASS is a stand-in for "MATERIAL(1)", and _B_SOLID is a stand-in for "IS_WALL, HEIGHT(12)".

# === Possible Future Features ===
# Property modifier macros
