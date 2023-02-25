import os
import random
from tile import Tile

class TilemapData():

    def __init__(self):
        self.load_file_paths()
        self.set_tiles()

        # red color inputs
        red_top = [1, 2, 5, 9, 10, 12, 13, 14, 17]
        red_right = [2, 3, 9, 10, 13, 14]
        red_bot = [10]
        red_left = [5, 6, 9, 10, 12, 13]

        # black color inputs
        black_top = [0]
        black_right = [0, 6, 7]
        black_bot = [0, 1, 4, 7, 8, 11, 15, 16, 17]
        black_left = [0, 3, 4]

        # black and red inputs
        black_red_top = [3, 4]
        red_black_top = [6, 7]
        red_black_right = [1, 4, 5, 8, 16, 17]
        black_red_bot = [2, 3]
        red_black_bot = [5, 6]
        red_black_left = [1, 2, 7, 8, 11, 17]

        #set background neighboars
        self.set_neighbours(0, black_bot, black_left, black_top, black_right)
        # set bush
        self.set_neighbours(1, red_bot, red_black_left, black_top, red_black_right)
        # set top right wall
        self.set_neighbours(2, red_bot, red_left, black_red_top, red_black_right)
        # set right wall
        self.set_neighbours(3, black_red_bot, red_left, black_red_top, black_right)
        # set bot right wall
        self.set_neighbours(4, black_red_bot, red_black_left, black_top, black_right)
        # set top left wall
        self.set_neighbours(5, red_bot, red_black_left, red_black_top, red_right)
        # set rihgt wall
        self.set_neighbours(6, red_black_bot, black_left, red_black_top, red_right)
        # set bot left wal
        self.set_neighbours(7, red_black_bot, black_left, black_top, red_black_right)
        # set tree bot
        self.set_neighbours(8, [9], red_black_left, black_top, red_black_right)
        # set tree top
        self.set_neighbours(9, red_bot, red_left, [8], red_right)
        # set red background
        self.set_neighbours(10, red_bot, red_left, red_top, red_right)
        # set temple bot left
        self.set_neighbours(11, [12], [15], black_top, red_black_right)
        # set temple left
        self.set_neighbours(12, red_bot, [18], [11], red_right)
        # set temple top
        self.set_neighbours(13, red_bot, red_left, [18], red_right)
        # set temple right
        self.set_neighbours(14, red_bot, red_left, [16], [18])
        # set temple bot
        self.set_neighbours(15, [18], [16], black_top, [11])
        # set temple bot right
        self.set_neighbours(16, [14], red_black_left, black_top, [15])
        # set wall
        self.set_neighbours(17, red_bot, red_black_left, black_top, red_black_right)
        #set temple middle
        self.set_neighbours(18, [13], [14], [15], [12])



    # get's all files from tile folder and sorts ascending
    def load_file_paths(self):
        tileFolder = "Artwork/NotStolenTiles"
        self.tilePaths = []

        # retrieve files
        for file in os.listdir(tileFolder):
            if file.lower().endswith(".png"):
                self.tilePaths.append(f"{tileFolder}/{file}")

        # sort files
        self.tilePaths.sort()

    def set_tiles(self):
        self.tiles = []

        for i, path in enumerate(self.tilePaths):
            tile = Tile(i, path)
            self.tiles.append(tile)

    #set all neighbours
    def set_neighbours(self, tileID, top, right, bot, left):
        self.set_top_neighbours(tileID, top)
        self.set_right_neighbours(tileID, right)
        self.set_bot_neighbours(tileID, bot)
        self.set_left_neighbours(tileID, left)

    # set right neighbours
    def set_right_neighbours(self, tileID, neighbourIDs):
        for id in neighbourIDs:
            self.tiles[tileID].rightNeighbours.add(self.tiles[id])

    # set left neighbours
    def set_left_neighbours(self, tileID, neighbourIDs):
        for id in neighbourIDs:
            self.tiles[tileID].leftNeighbours.add(self.tiles[id])

    # set top neighbours
    def set_top_neighbours(self, tileID, neighbourIDs):
        for id in neighbourIDs:
            self.tiles[tileID].topNeighbours.add(self.tiles[id])

    # set bot neighbours
    def set_bot_neighbours(self, tileID, neighbourIDs):
        for id in neighbourIDs:
            self.tiles[tileID].botNeighbours.add(self.tiles[id])

    def get_tiles(self):
        return self.tiles

    def get_tile_at(self, tileID) -> Tile:
        return self.tiles[tileID]

    def get_random_tile(self):
        return random.choice(self.tiles)

