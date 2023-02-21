import pygame
import random
from tile import Tile

class Cell():
    def __init__(self, row, col, possibleStates):
        self.possibleStates = possibleStates.copy()
        self.row = row
        self.col = col
        self.tile = None
        self.propagated = False
        self.collapsed = False

    def get_tile(self):
        return self.tile

    def set_tile(self, tile):
        self.tile = tile

    def collapse(self):
        tile = random.choice(self.possibleStates)
        self.set_tile(tile)
        self.collapsed = True
        self.propagated = True

    def draw(self, screen, x, y):
        if self.tile is not None:
            self.tile.draw(screen, x, y)

class WaveFunctionCollapse():
    def __init__(self, rows, cols, cellSize, allTiles):
        self.rowCount = rows;
        self.colCount = cols;
        self.cellSize = cellSize
        self.allTiles = allTiles
        self.grid = [[Cell(r, c, self.allTiles) for r in range(self.rowCount)] 
                                                for c in range(self.colCount)]

    def generate_tilemap(self):
        self.collapse_random_cell()
        #print(len(self.grid[0][0].possibleStates))
        #cell = self.find_cell_with_least_states()
        #if cell is not None:
        #    print(f"({cell.row}, {cell.col})")

        #self.propagate(cell)
        #if cell is not None:
        #    print(len(cell.possibleStates))

        
        # keep generating until there is no empty cells
        while True:
            cell = self.find_cell_with_least_states()
            result = self.propagate(cell)
            
            #if there is cell with no states, end algorithm
            if result == False:
                return False

            # cheack if grid is full
            if self.is_grid_full():
                 break 

        return True

    # Find not collapsed cell with least possible states, 
    # if there is the same amount of states, pciks state that has the most neighbours
    def find_cell_with_least_states(self):
        minCell = None
        minStateCount = 10000

        for row in self.grid:
            for cell in row:
                # if cell already collapsed, continue
                if cell.collapsed:
                    continue

                count = len(cell.possibleStates)

                if count == minStateCount:
                    minCellC = self.get_neighbour_count(minCell)
                    cellC = self.get_neighbour_count(cell)
                    if minCellC < cellC:
                        minCell = cell
                        minStateCount = count

                if count < minStateCount:
                    minCell = cell
                    minStateCount = count

        return minCell

    #returns neighbour count for a cell
    def get_neighbour_count(self, cell):
        count = 0

        # top neighbour
        top = self.get_top_neighbour(cell)
        if top is not None and top.tile is not None:
            count += 1

        # right neighbour
        right = self.get_right_neighbour(cell)
        if right is not None and right.tile is not None:
            count += 1

        # bottom neighbour
        bottom = self.get_bot_neighbour(cell)
        if bottom is not None and bottom.tile is not None:
            count += 1

        # left neighbour
        left = self.get_left_neighbour(cell)
        if left is not None and left.tile is not None:
            count += 1

        return count

    # checks if grid is full
    def is_grid_full(self):
        for row in self.grid:
            for cell in row:
                if cell.collapsed == False:
                    return False
        return True

    # collapses random tile
    def collapse_random_cell(self):
        row = random.choice(self.grid)
        cell = random.choice(row)
        cell.collapse()

    #propogates through tiles from start cell, collapse tile when needed
    def propagate(self, cell):
        row = cell.row
        col = cell.col

        #reset propogation state to deffault
        for r in self.grid:
            for cell in r:
                #skip if tile is already collapsed
                if cell.collapsed == False:
                    continue

                cell.propagated = False

        # apply BFS search algorith to propogate through cells
        propQueue = []

        def enqueue(cell):
            if cell is not None:
                if cell.propagated == False:
                    propQueue.append(cell)
                    startCell.propagated = True
 

        startCell = self.grid[row][col]
        enqueue(startCell)

        # loop until there all cells been propogated
        while propQueue:
            currCell = propQueue.pop(0)

            # get neighbouring cells
            topCell = self.get_top_neighbour(currCell)
            rightCell = self.get_right_neighbour(currCell)
            botCell = self.get_bot_neighbour(currCell)
            leftCell = self.get_left_neighbour(currCell)

            # propogate tile
            topPossi = self.get_top_possible_states(topCell)
            rightPossi = self.get_right_possible_states(rightCell)
            botPossi = self.get_bot_possible_states(botCell)
            leftPossi = self.get_left_possible_states(leftCell)
            allPosabilities = topPossi.union(topPossi, rightPossi, botPossi, leftPossi)
            print(f"Cell possabilities: {currCell.possibleStates}")
            print(f"All posabilities: {allPosabilities}")
            intersection = allPosabilities.intersection(currCell.possibleStates)
            print(f"Intersection: {intersection}")
            currCell.possibleStates = intersection

            # if current cell does not have any possible states, return algorithm false
            if len(currCell.possibleStates) == 0:
                print("Can't generate tile map as one of the cells don't have any states")
                return False
            
            # if there is only 1 possible state, collapse the tile
            if len(currCell.possibleStates) == 1:
                currCell.collapse()

            # queue neighbours
            enqueue(topCell)
            enqueue(rightCell)
            enqueue(botCell)
            enqueue(leftCell)
            break

        return True

    # returns top possible states
    def get_top_possible_states(self, topCell) -> set:
        topStates = set()
        if topCell is not None:
            for state in topCell.possibleStates:
                topStates = topStates.union(state.get_bot_possible_states())
        return topStates

    # returns right possible states
    def get_right_possible_states(self, rightCell) -> set:
        rightStates =  set()
        if rightCell is not None:
            for state in rightCell.possibleStates:
                rightStates = rightStates.union(state.get_left_possible_states())
        return rightStates

    # returns bot possible states
    def get_bot_possible_states(self, botCell) -> set:
        botStates =  set()
        if botCell is not None:
            for state in botCell.possibleStates:
                botStates = botStates.union(state.get_top_possible_states())
        return botStates

    # returns left possible states
    def get_left_possible_states(self, leftCell) -> set:
        leftStates =  set()
        if leftCell is not None:
            for state in leftCell.possibleStates:
                leftStates = leftStates.union(state.get_right_possible_states())
        return leftStates

    # returns right cell
    def get_right_neighbour(self, cell):
        if cell.col < self.colCount - 1:
            return self.grid[cell.row][cell.col+1]

        return None

    # returns left cell
    def get_left_neighbour(self, cell):
        if cell.col > 0:
            return self.grid[cell.row][cell.col-1]

        return None

    # returns top cell
    def get_top_neighbour(self, cell):
        if cell.row > 0:
            return self.grid[cell.row-1][cell.col]
        
        return None

    # returns bot cell
    def get_bot_neighbour(self, cell):
        if cell.row < self.rowCount - 1:
            return self.grid[cell.row+1][cell.col]

        return None
       
    # draw grid
    def draw_grid(self, screen, color=(0, 0, 0)):
        width = self.colCount * self.cellSize
        height = self.rowCount * self.cellSize
        # Draw the grid lines
        for row in range(0, height, self.cellSize):
            for col in range(0, width, self.cellSize):
                rect = pygame.Rect(col, row, self.cellSize, self.cellSize)
                pygame.draw.rect(screen, color, rect, 1)

    # clear grid
    def clear_grid(self):
        for r in range(self.rowCount):
            for c in range(self.colCount):
                self.grid[r][c].set_tile(None)

    # draw cells content
    def draw_cells(self, screen):
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                if cell is None:
                    continue

                x = c * self.cellSize
                y = r * self.cellSize
                cell.draw(screen, x, y)

    # custom print
    def __str__(self):
        string = ""

        for row in self.grid:
            for cell in row:
                if cell is not None:
                    string += f"{cell.tile.ID:3} "
                else:
                    string += f" -1 "
            string += "\n"
        return string
