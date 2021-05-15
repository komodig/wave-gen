import pygame

def draw_coordinate_cross(screen): 
    cross_color = pygame.Color(44,33,120)
    pygame.draw.line(screen, cross_color, (0, height/2), (width, height/2), 2)
    pygame.draw.line(screen, cross_color, (width/2, 0), (width/2, height), 2)

def draw_wave(screen):
    line_color = pygame.Color(55,155,55)
    spots = []

    x = -300
    while x < 300:
        y = x**2 - 10*x + 12
        spots.append((x+width/2,y+height/2))
        x += 2

    last_spot = None 
    for xy in spots:
        if last_spot is not None:
            pygame.draw.line(screen, line_color, last_spot, xy, 2)
            # print('({}:{} -> {}:{})'.format(last_spot[0], last_spot[1], xy[0], xy[1]))
        last_spot = xy

if __name__ == '__main__':
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
    draw_coordinate_cross(screen)
    draw_wave(screen)
    pygame.display.flip()

    while True:
        event = pygame.event.wait()
        if (event.type == pygame.QUIT or
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
            break

    pygame.quit()

