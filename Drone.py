import random
import numpy as np

class Drone:
    def __init__(self, coords, color):
        self.direction = random.choice([1, 2, 3, 4])
        self.current_coordinates = coords
        self.color = color
        self.straight_moves_left = random.choice([i for i in range(10)])
        self.beliefs = np.full((36, 1), 1/36)
        self.stored_beliefs = []

    def forward_coords(self):
        x = self.current_coordinates[0]; y = self.current_coordinates[1]
        dx = 1 if self.direction == 1 else -1 if self.direction == 3 else 0
        dy = 1 if self.direction == 2 else -1 if self.direction == 4 else 0
        return [x + dx, y + dy]
    
    def random_move(self):
        validMove = False
        while (not validMove):
            self.direction = random.choice([1, 2, 3, 4])
            if self.forward_coords()[0] > -1 and self.forward_coords()[0] < 20 and self.forward_coords()[1] > -1 and self.forward_coords()[1] < 20:
                self.current_coordinates = self.forward_coords()
                validMove = True

    def get_vote(self):
        vote = []
        for index, belief in enumerate(self.stored_beliefs):
            vote.append((belief[-1], index))
        vote.sort(key=lambda x: x[0], reverse=True)
        return [x[1] for x in vote]

    def update_beliefs(self, K, obs):
        rho_normal = np.linalg.norm(np.multiply(self.beliefs, np.dot(K, obs).reshape(-1, 1)))
        self.beliefs = np.multiply(self.beliefs, np.dot(K, obs).reshape(-1, 1)) / rho_normal

