import pygame
import random
from tile import Tile

class Grid():
    def __init__(self, rows, cols, cellSize):
        self.rowCount = rows;
        self.colCount = cols;
        self.width = rows * cellSize
        self.height = cols * cellSize
        self.cellSize = cellSize
        self.grid = [[None for i in range(self.rowCount)] 
                     for j in range(self.colCount)]

    # Tries to place tile, if the tile is not valid returns False
    def place_tile(self, tile, row, col):
        result = self.validate_placement(tile, row, col)

        if self.grid[row][col] is not None:
            self.remove_tile(row, col)

        self.grid[row][col] = tile
        return result

    def remove_tile(self, row, col):
        tile = self.grid[row][col]

        if tile is None:
            return

        index = row * self.colCount + col
        self.grid[row][col] = None

    # returns right neighbour
    def get_right_neighbour(self, row, col):
        if col < len(self.grid[0]) - 1:
            return self.grid[row][col+1]

        return None

    # return left neighbour
    def get_left_neighbour(self, row, col):
        if col > 0:
            return self.grid[row][col-1]

        return None

    # return top neighbour
    def get_top_neighbour(self, row, col):
        if row > 0:
            return self.grid[row-1][col]
        
        return None

    # return bot neighbour
    def get_bot_neighbour(self, row, col):
        if row < len(self.grid) -1:
            return self.grid[row+1][col]

        return None
       
    # validate tile placement with adjacent tiles
    def validate_placement(self, tile: Tile, row, col):
        # validate with left tile
        leftTile = self.get_left_neighbour(row, col)
        if leftTile is not None:
            if leftTile.ID not in tile.get_left_neighbours():
                return False

        # validate with right tile
        rightTile = self.get_right_neighbour(row, col)
        if rightTile is not None:
            if rightTile.ID not in tile.get_right_neighbours():
                return False

        # validate with bot tile
        botTile = self.get_bot_neighbour(row, col)
        if botTile is not None:
            if botTile.ID not in tile.get_bot_neighbours():
                return False

        # validate with top tile
        topTile = self.get_top_neighbour(row, col)
        if topTile is not None:
            if topTile.ID not in tile.get_top_neighbours():
                return False

        return True

    def get_cell_neighbour_count(self, row, col):
        count = 0

        #left neighbour
        left = self.get_left_neighbour(row, col)
        if left is not None:
            count += 1
        
        # right neighbour
        right = self.get_right_neighbour(row, col)
        if right is not None:
            count += 1

        # top neighbour
        top = self.get_top_neighbour(row, col)
        if top is not None:
            count += 1

        # bot neighbour
        bot = self.get_bot_neighbour(row, col)
        if bot is not None:
            count += 1

        return count

    def get_empty_cell_with_most_neighbours(self):
        counts = {}

        for r, row in enumerate(self.grid):
            for c, tile in enumerate(row):
                if tile is None:
                    count = self.get_cell_neighbour_count(r, c)

                    if count == 0:
                        continue

                    if count not in counts:
                        counts[count] = []

                    counts[count].append((r, c))
        
        if len(counts) == 0:
            return None

        largest_key = max(counts.keys())
        #take random one
        return random.choice(counts[largest_key])

    def at(self, row, col):
        return self.grid[row][col]

    def draw_grid(self, screen, color=(0, 0, 0)):
        # Draw the grid lines
        for row in range(0, self.height, self.cellSize):
            for col in range(0, self.width, self.cellSize):
                rect = pygame.Rect(col, row, self.cellSize, self.cellSize)
                pygame.draw.rect(screen, color, rect, 1)

    def clear_grid(self):
        for r in range(self.rowCount):
            for c in range(self.colCount):
                self.grid[r][c] = None

    def draw_tiles(self, screen):
        for r, row in enumerate(self.grid):
            for c, tile in enumerate(row):
                if tile is None:
                    continue
                x = c * self.cellSize
                y = r * self.cellSize
                tile.draw(screen, x, y)

    def __str__(self):
        string = ""

        for row in self.grid:
            for tile in row:
                if tile is not None:
                    string += f"{tile.ID:3} "
                else:
                    string += f" -1 "
            string += "\n"
        return string
