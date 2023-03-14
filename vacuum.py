import random
import enums.constants as con
import enums.walls as walls

class vacuum:
    def __init__(self, coords, color):
        self.direction = random.choice([1, 2, 3, 4])
        self.current_coordinates = coords
        self.color = color
        self.straight_moves_left = random.choice([i for i in range(10)])

    def forward_coords(self):
        x = self.current_coordinates[0]; y = self.current_coordinates[1]
        dx = 1 if self.direction == 1 else -1 if self.direction == 3 else 0
        dy = 1 if self.direction == 2 else -1 if self.direction == 4 else 0
        return [x + dx, y + dy]
    
    def random_move(self):
        validMove = False
        while (not validMove):
            self.direction = random.choice([1, 2, 3, 4])
            if self.forward_coords() not in walls.values:
                self.current_coordinates = self.forward_coords()
                validMove = True

    def move(self):
        if self.straight_moves_left > 0:
            if self.forward_coords() not in walls.values:
                self.current_coordinates = self.forward_coords()
                self.straight_moves_left -= 1
            else:
                self.random_move()
                self.straight_moves_left = random.choice([i for i in range(10)])
        else:
            self.straight_moves_left = random.choice([i for i in range(10)])
            self.random_move()
        return
