import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Four Choices Game")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)

# Define choices
learning_data = [{"Prompt": "Which letter?","Choices": ["s","d","f","g"], "Answers": ["d","f"]},{"Prompt": "??","Choices": ["z","d","f","g"], "Answers": ["d","f","g"]}]

# Set up fonts
font = pygame.font.Font(None, 36)
prompt_font = pygame.font.Font(None, 48)

import os
os.chdir(r"C:\Users\austin.tracy\LearningHub\games\multiple_choice\prompt_recordings")

import winsound
filename = r's.wav'
winsound.PlaySound(filename, winsound.SND_FILENAME)
# Main game loop
def main():
    learning_data_i = 0
    
    while True:
        choices = [
            {"text": learning_data[learning_data_i]["Choices"][0], "color": RED, "rect": pygame.Rect(0, 0, WIDTH // 2, HEIGHT // 2)},
            {"text": learning_data[learning_data_i]["Choices"][1], "color": GREEN, "rect": pygame.Rect(WIDTH // 2, 0, WIDTH // 2, HEIGHT // 2)},
            {"text": learning_data[learning_data_i]["Choices"][2], "color": BLUE, "rect": pygame.Rect(0, HEIGHT // 2, WIDTH // 2, HEIGHT // 2)},
            {"text": learning_data[learning_data_i]["Choices"][3], "color": YELLOW, "rect": pygame.Rect(WIDTH // 2, HEIGHT // 2, WIDTH // 2, HEIGHT // 2)}
        ]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for choice in choices:
                        if choice["rect"].collidepoint(event.pos):
                            print(f"Selected: {choice['text']}")
                    learning_data_i += 1
                            

        # Clear the screen
        screen.fill(WHITE)

        # Draw choices
        for choice in choices:
            pygame.draw.rect(screen, choice["color"], choice["rect"])
            text = font.render(choice["text"], True, BLACK)
            text_rect = text.get_rect(center=choice["rect"].center)
            screen.blit(text, text_rect)

        # Draw prompt box
        prompt_text = "Does this work with more text, a lot more text?"
        prompt = prompt_font.render(prompt_text, True, BLACK)
        prompt_rect = prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        
        # Create a slightly larger rectangle for the background
        background_rect = prompt_rect.inflate(20, 20)
        pygame.draw.rect(screen, LIGHT_GRAY, background_rect)
        pygame.draw.rect(screen, BLACK, background_rect, 2)  # Add a border
        
        # Draw the prompt text
        screen.blit(prompt, prompt_rect)

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    main()