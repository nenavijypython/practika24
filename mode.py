import pygame
import sys

def choose_mode(screen, font_large, font_small, background, block_color):
    mode = None
    mode_selected = False
    while not mode_selected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mode = "cpu"
                    mode_selected = True
                elif event.key == pygame.K_2:
                    mode = "two-player"
                    mode_selected = True
        screen.fill(background)
        mode_text = font_large.render("Select mode:", True, block_color)
        cpu_text = font_small.render("1: Play against CPU", True, block_color)
        player_text = font_small.render("2: Play two players", True, block_color)
        screen.blit(mode_text, (150, 150))
        screen.blit(cpu_text, (150, 250))
        screen.blit(player_text, (150, 300))
        pygame.display.flip()
    return mode
