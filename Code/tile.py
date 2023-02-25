import pygame

class Tile:
    ID = 0

    def __init__(self, tileID, path):
        self.ID = tileID
        self.path = path
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.rightNeighbours = set()
        self.leftNeighbours = set()
        self.topNeighbours = set()
        self.botNeighbours = set()

    # get available top neighbours
    def get_top_possible_states(self):
        return self.topNeighbours

    # get available bot neighbours
    def get_bot_possible_states(self):
        return self.botNeighbours

    # get available right neighbours
    def get_right_possible_states(self):
        return self.rightNeighbours

    # get available left neighbours
    def get_left_possible_states(self):
        return self.leftNeighbours

    # draw tile on screen
    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))

    # print id
    def __str__(self) -> str:
        return str(self.ID)
