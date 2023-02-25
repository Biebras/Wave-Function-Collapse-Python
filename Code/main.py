import pygame
from tilemap_data import TilemapData
from wave_function_collapse import WaveFunctionCollapse 

def main():
    #generation variables
    rows = 7
    cols = 10
    cell_size = 64

    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((cols * cell_size, rows * cell_size))
    backgroundColor = (200, 200, 200)
    screen.fill(backgroundColor)
    pygame.display.set_caption('Wave Function Collapse')

    #other initialisation
    clock = pygame.time.Clock()
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 9)

    #tilemap
    tilemapData = TilemapData(cell_size)
    tiles = tilemapData.get_tiles()
    wfc = WaveFunctionCollapse(rows, cols, cell_size, tiles, font, screen, backgroundColor, False)

    #wfc.generate_tilemap()

    # waint until user quits
    while True:
        # listen for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                # generate new tilemap on key press
                if event.key == pygame.K_g:
                    wfc.clear_grid()
                    result = wfc.generate_tilemap()

                    if result == False:
                        wfc.clear_grid()
                        wfc.generate_tilemap()

        # draw screen
        screen.fill(backgroundColor)       
        wfc.draw_cells()
        wfc.draw_grid()

        # update screen
        pygame.display.update()
        clock.tick(60)

# load main function
if __name__ == '__main__':
    main()
