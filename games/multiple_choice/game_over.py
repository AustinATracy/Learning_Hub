import pygame
import sys

def show_game_over_screen(score):
    # Initialize Pygame
    pygame.init()

    # Set up the display
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Game Over")

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    # Fonts
    font_large = pygame.font.Font(None, 72)
    font_medium = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 36)

    # Render text
    text_game_over = font_large.render("Game Over", True, RED)
    text_score = font_medium.render(f"Final Score: {score}", True, BLACK)
    text_play_again = font_small.render("Press ENTER to Play Again", True, GREEN)
    text_quit = font_small.render("Press ESC to Quit", True, RED)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "again"
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Fill the screen
        screen.fill(WHITE)

        # Draw text
        screen.blit(text_game_over, (width // 2 - text_game_over.get_width() // 2, 100))
        screen.blit(text_score, (width // 2 - text_score.get_width() // 2, 200))
        screen.blit(text_play_again, (width // 2 - text_play_again.get_width() // 2, 300))
        screen.blit(text_quit, (width // 2 - text_quit.get_width() // 2, 350))

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()