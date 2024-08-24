import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game with Celebration")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.Font(None, 64)
small_font = pygame.font.Font(None, 32)

# Particle class
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 5)
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.speed = random.uniform(2, 5)
        self.angle = random.uniform(0, 2 * math.pi)
        self.lifetime = random.randint(30, 60)

    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.lifetime -= 1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

def celebration_screen(correct_answers):
    particles = []
    celebration_running = True
    clock = pygame.time.Clock()

    while celebration_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Signal to quit the entire game
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                celebration_running = False

        screen.fill(BLACK)

        if len(particles) < 200:
            particles.append(Particle(width // 2, height // 2))

        for particle in particles[:]:
            particle.move()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)

        text = font.render("Well done!", True, WHITE)
        text_rect = text.get_rect(center=(width // 2, height // 2 - 50))
        screen.blit(text, text_rect)

        pygame.draw.circle(screen, YELLOW, (width // 2, height // 2 + 50), 30)
        pygame.draw.circle(screen, BLACK, (width // 2 - 10, height // 2 + 40), 5)
        pygame.draw.circle(screen, BLACK, (width // 2 + 10, height // 2 + 40), 5)
        pygame.draw.arc(screen, BLACK, (width // 2 - 15, height // 2 + 40, 30, 20), math.pi, 2 * math.pi, 3)

        answers_text = small_font.render(f"Correct answers: {correct_answers}", True, WHITE)
        answers_rect = answers_text.get_rect(center=(width // 2, height - 50))
        screen.blit(answers_text, answers_rect)

        pygame.display.flip()
        clock.tick(60)

    return True  # Signal to continue the main game

# def main_game():
#     game_running = True
#     correct_answers = 0

#     while game_running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 return False
#             # Handle other game events here

#         # Your main game logic here
#         # For example:
#         screen.fill(WHITE)
#         text = font.render("Main Game", True, BLACK)
#         text_rect = text.get_rect(center=(width // 2, height // 2))
#         screen.blit(text, text_rect)

#         # When you want to show the celebration screen:
#         # (This is just an example condition)
#         if pygame.time.get_ticks() % 5000 < 16:  # Every 5 seconds
#             correct_answers += 1
#             if not celebration_screen(correct_answers):
#                 return False

#         pygame.display.flip()

#     return True

# def game_loop():
#     while True:
#         if not main_game():
#             break
#     pygame.quit()

# if __name__ == "__main__":
#     game_loop()