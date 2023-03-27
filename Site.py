from random import randint
from enum import Enum
from perlin import generate_perlin_noise

DistributionType = Enum('DistributionType', ['RANDOM', 'BLOCK', 'PERLIN'])

class Site:
    """
    Class for the enviornment agents will perform site selection on.

    Attributes
    ----------
    distribution_pattern : enum/int
        The method for distributing the tiles
        0 -> Pure random
        1 -> Block
        2 -> perlin noise 
        #TODO: find more (?)

    board : 2d list of int
        The board itself with each tile belonging to one of the "features" (colors)
    
    """
    def __init__(self, distribution_pattern: int) -> None:
        self.distribution_pattern = distribution_pattern

        self.board = None

        if distribution_pattern == 0:
            self.board = self.__random_gen()
        elif distribution_pattern == 1:
            self.board = self.__block_gen()
        elif distribution_pattern == 2:
            self.board = self.__perlin_gen()

    def __str__(self):
        output = ""
        for row_index in range(len(self.board)):
            output += "\n|"
            for col_index in range(len(self.board[row_index])):
                output += f"{self.board[row_index][col_index]}|"
        return output


    def __random_gen(self):
        """Generates 20x20 environment board with complete random distribution"""
        return [[randint(0,2) for col in range(20)] for row in range(20)]

    def __block_gen(self):
        """Generates 20x20 environment board using the block distribution demonstrated in the reasearch paper"""
        pass

    def __perlin_gen(self):
        """Generates 20x20 environment board using perlin noise to create a natural-looking environment"""
        perlin_map = generate_perlin_noise(20, 20, 5, 0.99, 5)
        # print(perlin_map)
        for row_index in range(len(perlin_map)):
            for col_index in range(len(perlin_map[row_index])):
                if perlin_map[row_index][col_index] < .6:
                    perlin_map[row_index][col_index] = 0
                elif perlin_map[row_index][col_index] < 0.9:
                    perlin_map[row_index][col_index] = 1
                else:
                    perlin_map[row_index][col_index] = 2
        print(perlin_map)
        
        return perlin_map