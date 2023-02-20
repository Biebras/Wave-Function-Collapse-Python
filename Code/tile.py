import pygame

class Tile:
    ID = 0

    def __init__(self, tileID, path, superposition):
        self.ID = tileID
        self.path = path
        self.image = pygame.image.load(path)
        self.rightNeighbours = set()
        self.leftNeighbours = set()
        self.topNeighbours = set()
        self.botNeighbours = set()

    # sets neighbours from input
    def set_neighbours(self, mapInput):
        def set_adjacent_neighbours(row, col):
            if col > 0:
                self.leftNeighbours.add(mapInput[row][col-1])
            if col < len(mapInput[row]) - 1:
                self.rightNeighbours.add(mapInput[row][col+1])
            if row > 0:
                self.topNeighbours.add(mapInput[row-1][col])
            if row < len(mapInput) - 1:
                self.botNeighbours.add(mapInput[row+1][col])

        for row in range(len(mapInput)):
            for col in range(len(mapInput[row])):
                if self.ID == mapInput[row][col]:
                    set_adjacent_neighbours(row, col)

    # get available top neighbours
    def get_top_neighbours(self):
        return self.topNeighbours

    # get available bot neighbours
    def get_bot_neighbours(self):
        return self.botNeighbours

    # get available right neighbours
    def get_right_neighbours(self):
        return self.rightNeighbours

    # get available left neighbours
    def get_left_neighbours(self):
        return self.leftNeighbours

    # draw tile on screen
    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))
