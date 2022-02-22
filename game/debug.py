import pygame
pygame.init()
font = pygame.font.Font(None, 30)

def debug(message, x=10, y=10) -> None:
    screen = pygame.display.get_surface()
    debug_surface = font.render(str(message), True, (255,255,255))
    debug_rect = debug_surface.get_rect(topleft=(x, y))
    pygame.draw.rect(screen, (0,0,0), debug_rect)
    screen.blit(debug_surface, debug_rect)