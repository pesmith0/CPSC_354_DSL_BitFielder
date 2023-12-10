// this test program requires a header generated using:
// python3 src/bitfielder_parser.py docs/example_1.txt > docs/example_output.h

// to compile this program:
// g++ test.cpp
// or:
// gcc test.c

#include "example_output.h"
// #include <stdio.h> // c
#include <iostream> // cpp

int main(){
    BlockID grass_block = B_GRASS;

    // // c:
    // printf("Grass block's material field: %d\n", BLOCK_MATERIAL(grass_block));
    // printf("Grass block's is_air field: %d\n", BLOCK_IS_AIR(grass_block));

    // cpp:
    std::cout << "Grass block's material field: " << BLOCK_MATERIAL(grass_block) << std::endl;
    std::cout << "Grass block's is_air field: " << BLOCK_IS_AIR(grass_block) << std::endl;
}