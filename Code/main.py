import pygame
from tilemap_data import TilemapData
from wave_function_collapse import WaveFunctionCollapse 

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((768, 768))
    backgroundColor = (200, 200, 200)
    screen.fill(backgroundColor)
    pygame.display.set_caption('Wave Function Collapse')
    clock = pygame.time.Clock()
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 9)

    #tilemap
    tilemapData = TilemapData()
    tiles = tilemapData.get_tiles()
    wfc = WaveFunctionCollapse(12, 10, 64, tiles)

    # wfc generation
    wfc.generate_tilemap()

    #wfc.collapse_random_cell()
    #cell = wfc.find_cell_with_least_states()

    # waint until user quits
    while True:
        # if player quits, exit application
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    wfc.clear_grid()
                    wfc.generate_tilemap()

        screen.fill(backgroundColor)       
        wfc.draw_cells(screen)
        #wfc.draw_grid(screen, font)

        pygame.display.update()
        clock.tick(60)

# load main function
if __name__ == '__main__':
    main()
