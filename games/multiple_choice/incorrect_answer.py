import pygame
import sys

def show_incorrect_screen(num_thumbs_down, correct_answer,thumbs_down_image):
    # Initialize Pygame
    pygame.init()

    # Set up the display
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Incorrect Answer")

    # Colors
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)

    # Fonts
    font_large = pygame.font.Font(None, 72)
    font_small = pygame.font.Font(None, 48)

    # Render text
    text_incorrect = font_large.render("Incorrect", True, RED)
    text_correct = font_small.render(f"Correct answer: {correct_answer}", True, BLACK)

    # Load and scale thumbs down image
    thumbs_down = pygame.transform.scale(thumbs_down_image, (100, 100))

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                running = False

        # Fill the screen
        screen.fill(WHITE)

        # Draw text
        screen.blit(text_incorrect, (width // 2 - text_incorrect.get_width() // 2, 100))
        screen.blit(text_correct, (width // 2 - text_correct.get_width() // 2, 200))

        # Draw thumbs down icons
        for i in range(num_thumbs_down):
            screen.blit(thumbs_down, (width // 2 - (num_thumbs_down * 110) // 2 + i * 110, 300))

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    return True