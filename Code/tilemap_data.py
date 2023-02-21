import os
import random
from tile import Tile

class TilemapData():

    def __init__(self):
        # tileset input, AI should generate room following rules set by input
        self.input = [[ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                 [ 0,  0,  1,  2,  2,  2,  3,  0,  0,  0],
                 [ 0,  0,  4,  5,  6,  7,  8,  2,  3,  0],
                 [ 0,  0,  4,  9, 10, 11, 12, 13, 14,  0],
                 [ 0,  0,  4, 15, 16, 17, 18, 19, 14,  0],
                 [ 0,  1, 20, 21, 22, 23, 24, 25, 26,  0],
                 [ 0,  4, 27, 28, 29, 11, 28,  9, 14,  0],
                 [ 0,  4, 30, 31, 32, 33, 34, 23, 14,  0],
                 [ 0,  4, 35, 36, 17, 37, 37, 38, 14,  0],
                 [ 0, 39, 40, 41, 42, 43, 44, 44, 45,  0],
                 [ 0,  1, 46, 22, 23,  8,  2,  3,  0,  0],
                 [ 0,  4,  5, 47, 11, 28, 48, 14,  0,  0],
                 [ 0,  4, 49, 50, 32, 34, 51, 14,  0,  0],
                 [ 0, 52, 21, 41, 53, 54, 55, 14,  0,  0],
                 [ 0,  4, 56, 57, 18, 19, 43, 45,  0,  0],
                 [ 0, 39, 44, 44, 44, 44, 45,  0,  0,  0],
                 [ 0,  0,  0,  0,  0,  0,  0,  0,  0 ,  0]]
       
        self.set_file_paths()
        self.set_tiles()

    # get's all files from tile folder and sorts ascending
    def set_file_paths(self):
        tileFolder = "Artwork/Tiles"
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

        for tile in self.tiles:
            tile.set_neighbours(self.input, self.tiles)

    def get_tiles(self):
        return self.tiles

    def get_tile_at(self, tileID) -> Tile:
        return self.tiles[tileID]

    def get_random_tile(self):
        return random.choice(self.tiles)

