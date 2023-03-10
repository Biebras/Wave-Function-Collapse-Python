import pygame
import random

class Cell():
    def __init__(self, row, col, possibleStates):
        self.possibleStates = set(possibleStates.copy())
        self.row = row
        self.col = col
        self.tile = None
        self.propagated = False
        self.collapsed = False

    def get_tile(self):
        return self.tile

    def set_tile(self, tile):
        self.tile = tile

    # collapse cell with random tile into singularity
    def collapse(self):
        tile = random.choice(list(self.possibleStates))
        self.collapse_with(tile.ID)

    # collapse cell with specific tile into singularity
    def collapse_with(self, index):
        tmp = list(self.possibleStates)

        tile = tmp[0]
        for t in tmp:
            if t.ID == index:
                tile = t

        self.set_tile(tile)
        self.collapsed = True
        self.propagated = True
        self.possibleStates.clear()
        self.possibleStates.add(tile)

    def cord(self):
        return (self.row, self.col)

    def draw(self, screen, x, y):
        if self.tile is not None:
            self.tile.draw(screen, x, y)

class WaveFunctionCollapse():
    def __init__(self, rows, cols, cellSize, allTiles, font, screen, backgroundColor, debug = False):
        self.rowCount = rows;
        self.colCount = cols;
        self.cellSize = cellSize
        self.allTiles = allTiles
        self.screen = screen
        self.font = font
        self.backgroundColor = backgroundColor
        self.debug = debug

        self.grid = [[Cell(r, c, self.allTiles) for c in range(self.colCount)] 
                                                for r in range(self.rowCount)]
        
    def update_screen(self):
        self.screen.fill(self.backgroundColor)
        self.draw_cells();
        self.draw_grid();
        pygame.display.update()

    # use wave function collapse algorithm to generate tilemap
    def generate_tilemap(self):
        maxHeight = random.randint(-1, 3)

        if maxHeight != -1:
            for col in range(self.colCount):
                self.grid[maxHeight][col].collapse_with(10)
                if self.debug:
                    self.update_screen()
                    pygame.time.wait(50)
        else:
            self.collapse_random_cell()

        
        # keep generating until there is no empty cells
        while True:
            cell = None

            # cheack if grid is full
            if self.is_grid_full():
                 break 
            
            # propogate multiple times, to ensure that we collapse least possible states
            for _ in range(4):
                cell = self.find_cell_with_least_states()
                
                if cell is None:
                    break

                result = self.propagate(cell)
            
                #if there is cell with no states, end algorithm
                if result == False:
                    return False

            least_states = self.find_cell_with_least_states()

            # compare least states with cell that was propogated and collapse the one with least states
            if cell is not None:
                if least_states is not None:
                    if len(least_states.possibleStates) < len(cell.possibleStates):
                        cell = least_states

                cell.collapse()

        return True
    
    #propogates through tiles from start cell, collapse tile when needed
    def propagate(self, startCell):

        #reset propogation state to deffault
        for row in self.grid:
            for cell in row:
                cell.propagated = False

        # apply BFS search algorith to propogate through cells
        propQueue = []

        def enqueue(cell):
            if cell is not None:
                if cell.propagated == False and cell.collapsed == False:
                    propQueue.append(cell)
                    cell.propagated = True

        enqueue(startCell)

        # loop until there all cells been propogated
        while propQueue:
            currCell = propQueue.pop(0)

            if currCell.collapsed == False:
                topPossi = self.get_top_possible_states(currCell)
                rightPossi = self.get_right_possible_states(currCell)
                botPossi = self.get_bot_possible_states(currCell)
                leftPossi = self.get_left_possible_states(currCell)
                intersection = topPossi.intersection(topPossi, rightPossi, botPossi, leftPossi)
                currCell.possibleStates = intersection

                # if current cell does not have any possible states, return algorithm false
                if len(currCell.possibleStates) == 0:
                    print("Can't generate tile map as one of the cells don't have any states")
                    return False
                
                # if there is only 1 possible state, collapse the tile
                if len(currCell.possibleStates) == 1:
                    currCell.collapse()

                topCell = self.get_top_neighbour(currCell)
                rightCell = self.get_right_neighbour(currCell)
                botCell = self.get_bot_neighbour(currCell)
                leftCell = self.get_left_neighbour(currCell)

            # queue neighbours
            enqueue(topCell)
            enqueue(rightCell)
            enqueue(botCell)
            enqueue(leftCell)

            if self.debug:
                self.update_screen()
                pygame.time.wait(1)

        return True

    # Find not collapsed cell with least possible states, 
    # if there is the same amount of states, pciks state that has the most neighbours
    def find_cell_with_least_states(self):
        least_states = float('inf')
        most_neighbors = -1
        result_cell = None

        for row in self.grid:
            for cell in row:
                if cell.collapsed == True:
                    continue

                cell_states = len(cell.possibleStates)
                if cell_states < least_states:
                    least_states = cell_states
                    most_neighbors = self.get_neighbour_count(cell)
                    result_cell = cell
                elif cell_states == least_states:
                    neighbor_count = self.get_neighbour_count(cell)
                    if neighbor_count > most_neighbors:
                        most_neighbors = neighbor_count
                        result_cell = cell

        return result_cell

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
        return cell

    # returns top possible states
    def get_top_possible_states(self, cell) -> set:
        topStates = set()
        topCell = self.get_top_neighbour(cell)
        if topCell is not None:
            for state in topCell.possibleStates:
                topStates = topStates.union(state.get_bot_possible_states())

        if len(topStates) == 0:
            topStates = set(self.allTiles)

        return topStates

    # returns right possible states
    def get_right_possible_states(self, cell) -> set:
        rightStates =  set()
        rightCell = self.get_right_neighbour(cell)
        if rightCell is not None:
            for state in rightCell.possibleStates:
                rightStates = rightStates.union(state.get_left_possible_states())
        
        if len(rightStates) == 0:
            rightStates = set(self.allTiles)

        return rightStates

    # returns bot possible states
    def get_bot_possible_states(self, cell) -> set:
        botStates =  set()
        botCell = self.get_bot_neighbour(cell)
        if botCell is not None:
            for state in botCell.possibleStates:
                botStates = botStates.union(state.get_top_possible_states())

        if len(botStates) == 0:
            botStates = set(self.allTiles)

        return botStates

    # returns left possible states
    def get_left_possible_states(self, cell) -> set:
        leftStates =  set()
        leftCell = self.get_left_neighbour(cell)
        if leftCell is not None:
            for state in leftCell.possibleStates:
                leftStates = leftStates.union(state.get_right_possible_states())

        if len(leftStates) == 0:
            leftStates = set(self.allTiles)

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
    def draw_grid(self, color=(0, 0, 0)):
        for row in range(self.rowCount):
            for col in range(self.colCount):
                cell = self.grid[row][col]
                x = col * self.cellSize
                y = row * self.cellSize

                cord = f"({row}, {col})"
                stateCount = f"{len(cell.possibleStates)}"

                if cell.propagated == True:
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 0)

                if cell.collapsed == False:
                    rect = pygame.Rect(x, y, self.cellSize, self.cellSize)
                    pygame.draw.rect(self.screen, color, rect, 1)
                    text_states = self.font.render(stateCount, False, (0, 0, 0))
                    self.screen.blit(text_states, (x + 3, y))
                    text_cord = self.font.render(cord, False, (0, 0, 0))
                    self.screen.blit(text_cord, (x + 3, y + 15))

    # clear grid
    def clear_grid(self):
        for r in range(self.rowCount):
            for c in range(self.colCount):
                self.grid[r][c].collapsed = False
                self.grid[r][c].possibleStates = set(self.allTiles)
                self.grid[r][c].set_tile(None)

    # draw cells content
    def draw_cells(self):
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                if cell is None:
                    continue

                x = c * self.cellSize
                y = r * self.cellSize
                cell.draw(self.screen, x, y)

    # custom print
    def __str__(self):
        string = ""

        for row in self.grid:
            for cell in row:
                if cell is not None:
                    if cell.tile is not None:
                        string += f"{cell.tile.ID:3} "
                    else:
                        string += f" -1 "
            string += "\n"
        return string
