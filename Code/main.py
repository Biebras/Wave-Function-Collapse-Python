import pygame
from tilemap_data import TilemapData
from wave_function_collapse import WaveFunctionCollapse 

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((512, 512))
    backgroundColor = (200, 200, 200)
    screen.fill(backgroundColor)
    pygame.display.set_caption('Wave Function Collapse')
    clock = pygame.time.Clock()

    #tilemap
    tilemapData = TilemapData()
    tiles = tilemapData.get_tiles()
    wfc = WaveFunctionCollapse(16, 16, 32, tiles)

    # collapse random tile to start algorithm
    wfc.collapse_random_cell()

    # waint until user quits
    while True:
        # if player quits, exit application
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        wfc.draw_grid(screen)

        pygame.display.update()
        clock.tick(60)

# load main function
if __name__ == '__main__':
    main()
