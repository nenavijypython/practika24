import pygame
import sys

def choose_rounds(screen, font_large, font_small, background, block_color):
    rounds = 3  # Default value
    rounds_selected = False
    while not rounds_selected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    rounds = 5
                    rounds_selected = True
                elif event.key == pygame.K_3:
                    rounds = 15
                    rounds_selected = True
                elif event.key == pygame.K_2:
                    rounds = 10
                    rounds_selected = True
        screen.fill(background)
        rounds_text = font_large.render("Select number of rounds:", True, block_color)
        rounds_5_text = font_small.render("1: Play 5 rounds", True, block_color)
        rounds_10_text = font_small.render("2: Play 10 rounds", True, block_color)
        rounds_15_text = font_small.render("3: Play 15 rounds", True, block_color)
        screen.blit(rounds_text, (50, 150))
        screen.blit(rounds_5_text, (50, 250))
        screen.blit(rounds_10_text, (50, 300))
        screen.blit(rounds_15_text, (50, 350))
        pygame.display.flip()
    return rounds
