import os
import random
from tile import Tile

class TilemapData():

    def __init__(self):
        # tileset input, AI should generate room following rules set by input
        self.input = [[  0,  0,  0,  0,  0,  0,  0],
                      [  0,  0,  1,  0,  2,  0,  0],
                      [  0,  3,  4,  4,  5,  0,  0],
                      [  6,  7,  8,  8,  9,  0,  0],
                      [ 10,  7,  8,  8,  9,  6,  6],
                      [ 10,  7,  8,  8,  9, 10, 10]]
        
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

