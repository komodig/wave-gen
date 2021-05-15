import pygame
from libwave import POS_MAX

def _draw_coordinate_cross(screen, width, height):
    cross_color = pygame.Color(44,33,120)
    pygame.draw.line(screen, cross_color, (0, height/2), (width, height/2), 2)
    pygame.draw.line(screen, cross_color, (width/2, 0), (width/2, height), 2)

def _draw_lines(screen, vals, rgb, width, height):
    r, g, b = rgb
    line_color = pygame.Color(r, g, b)
    last_spot = None

    vtup = zip(list(range(width)), vals[:width])
    for _xy in vtup:
        xy = (_xy[0], _xy[1] * (1/(2*POS_MAX/height)) + height/2) # scale amplitude to graph-size
        if last_spot is not None:
            pygame.draw.line(screen, line_color, last_spot, xy, 2)
            print('({}:{} -> {}:{})'.format(last_spot[0], last_spot[1], xy[0], xy[1]))
        last_spot = xy

def draw_wave(f1, f2):
    pygame.init()

    width = 1024
    height = 768
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Monkey Fever')
    pygame.mouse.set_visible(1)

    background = pygame.Surface(screen.get_size())
    background = background.convert()

    background.fill((20, 20, 20))
    screen.blit(background, (0, 0))
    _draw_coordinate_cross(screen, width, height)
    _draw_lines(screen, f1, [55, 155, 55], width, height)
    _draw_lines(screen, f2, [166, 66, 66], width, height)

    pygame.display.flip()

    while True:
        event = pygame.event.wait()
        if (event.type == pygame.QUIT or
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
            break

    pygame.quit()

