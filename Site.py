from operator import is_
from random import randint, random
from enum import Enum

from numpy import block
from perlin import generate_perlin_noise
from itertools import chain

import math

DistributionType = Enum('DistributionType', ['RANDOM', 'BLOCK', 'PERLIN'])

class Site:
    """
    Class that the enviornment agents will perform site selection on.

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
    def __init__(self, distribution_pattern: int,  target_percentage = None, variance = None) -> None:
        self.distribution_pattern = distribution_pattern
        self.target_percentage = target_percentage
        self.board = None
        self.current_percentage = None
        self.variance = 5

        if distribution_pattern == 0:
            self.__random_gen()
        elif distribution_pattern == 1:
            self.__block_gen()
        elif distribution_pattern == 2:
            self.__perlin_gen()

        self.get_current_percentage()

    def __str__(self):
        output = ""
        for row_index in range(len(self.board)):
            output += "\n|"
            for col_index in range(len(self.board[row_index])):
                output += f"{self.board[row_index][col_index]}|"
        return output

    def get_current_percentage(self):
        """Returns the make-up of the board by percentage of each feature. Given by a three value list, with the index corasponding to feature."""
        self.current_percentage = [list(chain.from_iterable(self.board)).count(feature_index)/400 for feature_index in range(0,3)]
        # print(self.current_percentage)
        return self.current_percentage

    def __random_gen(self):
        """Generates 20x20 environment board with complete random distribution"""
        if self.target_percentage is None:
            return [[randint(0,2) for col in range(20)] for row in range(20)]
        else:
            self.board = [[random() for col in range(20)] for row in range(20)]
            for row_index in range(20):
                for col_index in range(20):
                    random_float = random()
                    if random_float < (self.target_percentage[0] / 100):
                        self.board[row_index][col_index] = 0
                    elif random_float < ((self.target_percentage[0] / 100) + (self.target_percentage[1] / 100)):
                         self.board[row_index][col_index] = 1
                    else:
                         self.board[row_index][col_index] = 2

    def __block_gen(self):
        """Generates 20x20 environment board using the block distribution described in the reasearch paper"""
        # self.target_percentage = (65, 30, 5)
        self.target_percentage = (50, 25, 25)
        self.variance = 5

        self.board = [[0 for _ in range(20)] for _ in range(20)]
        ratio_met = [False, False, False]
        #Set all values to 0

        #Make a large block of 1 and 2 on 0 background
        block_size1 = int(math.sqrt(400*(self.target_percentage[1]/100)))
        block_size2 = int(math.sqrt(400*(self.target_percentage[2]/100)))
        starting_point1 = randint(0, 20-block_size1)
        starting_point2 = randint(0, 20-block_size2)

        #block 1
        for row_index in range(starting_point1, starting_point1 + block_size1):
            for col_index in range(starting_point1, starting_point1 + block_size1):
                self.board[row_index][col_index] = 1

        #block 2
        for row_index in range(starting_point2, starting_point2 + block_size2):
            for col_index in range(starting_point2, starting_point2 + block_size2):
                self.board[row_index][col_index] = 2

        while (ratio_met != [True, True, True]):
            for feature_num in range(1,3):
                self.__increment_block(self.board, feature_num)
                ratio_met = self.__check_ratio_status()
            if ratio_met == [False, True, True]:
                self.__increment_bg(self.board)


        return self.board

    def __perlin_gen(self):
        """Generates 20x20 environment board using perlin noise to create a natural-looking environment"""
        if self.target_percentage is not None:
            raise NotImplementedError("Target ratio not yet implemented with perlin distribution")

        perlin_map = generate_perlin_noise(20, 20, 5, 0.99, 5)
        # print(perlin_map)
        for row_index in range(len(perlin_map)):
            for col_index in range(len(perlin_map[row_index])):
                if perlin_map[row_index][col_index] < .6:
                    perlin_map[row_index][col_index] = 0
                elif perlin_map[row_index][col_index] < 0.8:
                    perlin_map[row_index][col_index] = 1
                else:
                    perlin_map[row_index][col_index] = 2
        
        self.board = perlin_map

    def __check_ratio_status(self):
        """Returns a 3-element list of bools, each indicating whether that feature is within the needed threshold."""
        output = [None, None, None]
        for feature_num in range(3):
            print(f"feature number: {feature_num}\n\tcurrent percentage: {self.get_current_percentage()[feature_num] * 100}\n\tLower boound:{self.target_percentage[feature_num] - self.variance}\n\tUpper bound: {self.target_percentage[feature_num] + self.variance}")
            if self.get_current_percentage()[feature_num] * 100 >= self.target_percentage[feature_num] - self.variance \
                and self.get_current_percentage()[feature_num] * 100 <= self.target_percentage[feature_num] + self.variance:
                    print(f"{feature_num} percentage is good")
                    output[feature_num] = True
            else: output[feature_num] = False
        return output


    def __increment_block(self, block_index: int):
        """Adds or removes a block of the given feature"""
        #If percentage is too low, we need to add a block
        if self.get_current_percentage()[block_index] * 100 < self.target_percentage[block_index] - self.variance:
            candidates = get_grow_candidates(self.board, block_index)
            #Change random candidate to desired feature type
            if candidates != []: 
                random_candidate_coords = candidates[randint(0, len(candidates) - 1)]
                self.board[random_candidate_coords[0]][random_candidate_coords[1]] = block_index
            else:
                print("no grow candidates!")
        
        #If percentage is too high, we need to remove a block
        elif self.get_current_percentage()[block_index] * 100 > self.target_percentage[block_index] + self.variance:
            candidates = get_shrink_candidates(self.board, block_index)
            if candidates != []: 
                random_candidate_coords = candidates[randint(0, len(candidates) - 1)]
                self.board[random_candidate_coords[0]][random_candidate_coords[1]] = 0

    def __increment_bg(self):
        """Adds to random featuer if bg is too big, shrinks random feature if bg is too small"""
        #If background feature is too low, then add more
        if self.get_current_percentage()[0] * 100 < self.target_percentage[0] - self.variance:
            print("Adding to bg")
            candidates = get_shrink_candidates(self.board, randint(1,2))
            #Change random candidate to desired feature type
            if candidates != []: 
                random_candidate_coords = candidates[randint(0, len(candidates) - 1)]
                self.board[random_candidate_coords[0]][random_candidate_coords[1]] = 0
            else:
                print("no grow candidates!")
        
        #If percentage is too high, we need to remove a block
        elif self.get_current_percentage()[0] * 100 > self.target_percentage[0] + self.variance:
            print("Removing from bg")
            recipient = randint(1,2)
            candidates = get_grow_candidates(self.board, recipient)
            if candidates != []: 
                random_candidate_coords = candidates[randint(0, len(candidates) - 1)]
                self.board[random_candidate_coords[0]][random_candidate_coords[1]] = recipient



def get_grow_candidates(board, feature_num):
    grow_candidates = []
    for row_index in range(1, 19):
        for col_index in range(1, 19):
            if board[row_index][col_index] == feature_num: 
                add_grow_candidates(board, feature_num, row_index, col_index, grow_candidates)
    return grow_candidates

def add_grow_candidates(board, feature_index, row_index, col_index, candidate_list):
    for row_variation in range(-1, 2, 2):
        for col_variation in range(-1, 2, 2):
            if board[row_index + row_variation][col_index + col_variation] != feature_index:
                candidate_list.append([row_index + row_variation, col_index + col_variation])

def get_shrink_candidates(board, feature_num):
    shrink_candidates = []
    for row_index in range(1, 19):
        for col_index in range(1, 19):
            if board[row_index][col_index] == feature_num: 
                add_shrink_candidates(board, feature_num, row_index, col_index, shrink_candidates)
    return shrink_candidates

def add_shrink_candidates(board, feature_index, row_index, col_index, candidate_list):
    for row_variation in range(-1, 2, 2):
        for col_variation in range(-1, 2, 2):
            if board[row_index + row_variation][col_index + col_variation] != feature_index:
                candidate_list.append([row_index, col_index])
    