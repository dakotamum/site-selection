from random import randint

class Enviornment:
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
    
    feature_count : int
        The number of "features" (colors) to be displayed

    board : 2d list of int
        The board itself with each tile belonging to one of the "features" (colors)

    

    
    """
    def __init__(self, distribution_pattern: int, feature_count: int) -> None:
        self.distribution_pattern = distribution_pattern
        self.feature_count = feature_count

        self.board = None

        if distribution_pattern == 0:
            self.board = __random_gen(feature_count)
        elif distribution_pattern == 1:
            self.board = __block_gen(feature_count)
        elif distribution_pattern == 2:
            self.board = __perlin_gen(feature_count)

    def __str__(self):
        output = ""
        for row_index in self.board:
            output += "\n|"
            for col_index in self.board:
                output += f"{self.board[row_index][col_index]}|"
        return output


def __random_gen(feature_count: int):
    """Generates 20x20 environment board with complete random distribution"""
    return [[randint(0,feature_count) for col in range(20)] for row in range(20)]

def __block_gen(feature_count: int):
    """Generates 20x20 environment board using the block distribution demonstrated in the reasearch paper"""
    pass

def __perlin_gen(feature_count: int):
    """Generates 20x20 environment board using perlin noise to create a natural-looking environment"""
    pass