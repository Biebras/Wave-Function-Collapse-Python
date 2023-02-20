import pygame
import neat
from tilemap_data import Tile, TilemapData
from grid import Grid

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((512, 512))
    backgroundColor = (200, 200, 200)
    screen.fill(backgroundColor)
    pygame.display.set_caption('Basic Pygame program')
    clock = pygame.time.Clock()

    #tilemap
    tilemapData = TilemapData()
    tiles = tilemapData.get_tiles()
    grid = Grid(16, 16, 32)

    # waint until user quits
    while True:
        # if player quits, exit application
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()
        clock.tick(600)

# load main function
if __name__ == '__main__':
    main()
