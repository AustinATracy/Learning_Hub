from datetime import datetime
import pygame
import random
import sys
import winsound

import pandas as pd

from celebration_screen import celebration_screen 
from game_over import show_game_over_screen
from incorrect_answer import show_incorrect_screen
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

# Set up fonts
font = pygame.font.Font(None, 128)
prompt_font = pygame.font.Font(None, 48)

thumbs_down_image = pygame.image.load(r"C:\Users\austin.tracy\LearningHub\games\multiple_choice\deny-2028634_1280.png")

import os
os.chdir(r"C:\Users\austin.tracy\LearningHub\games\multiple_choice\prompt_recordings")

def get_letters(df_letters):
    df_letters["Total Priority"] = df_letters[["Priority"]].cumsum()
    df_letters_condensed = df_letters.loc[df_letters["Total Priority"] <= 40]
    letters = df_letters_condensed["Correct Answer"].to_list()
    df_letters_condensed = df_letters_condensed.loc[df_letters_condensed["Other Question Padding"] <= 0]
    max_priority = df_letters_condensed["Priority"].max()
    df_letters_condensed = df_letters_condensed.loc[df_letters_condensed["Priority"] == max_priority]
    correct_answer_index = random.choice(df_letters_condensed.index)
    correct_answers = [df_letters_condensed.loc[correct_answer_index]["Correct Answer"]]
    df_letters.drop("Total Priority",axis=1)
    return letters, correct_answers

def set_up_a_round(df_letters):
        letters, correct_letters = get_letters(df_letters)
        if correct_letters[0] == "c":
            if random.random() > 0:
                audio_letter = "k"
                correct_letters = random.choice([["c(a)","k","q"],["c(o)","k","q"],["c(u)","k","q"]])
            else:
                audio_letter = "s"
                correct_letters = random.choice([["c(e)","s"],["c(i)","s"]])
        elif correct_letters[0] == "q":
            audio_letter = "k"
            correct_letters = ["q","c","k"]
        elif correct_letters[0] == "k":
            audio_letter = "k"
            correct_letters = ["k","c","q"]
        elif correct_letters[0] == "s":
            audio_letter = "s"
            correct_letters = ["s","c"]
        else:
            audio_letter = correct_letters[0]

        random_letters = random.choices(letters,k=3)
        random_letters += correct_letters
        if len(letters) >= 4:
            while True:
                random_letters = list(set(random_letters))
                random_letters_length = len(random_letters)
                if random_letters_length < 4:
                    letters = list(set(letters).difference(random_letters))
                    random_letters += random.choices(letters,k=4-random_letters_length)
                else:
                    break
        random_letters = list(random_letters)
        
        filename = f'{audio_letter}.wav'
        return random_letters, correct_letters, filename
    

# Main game loop
def main():
    df_letters = pd.read_csv(r"C:\Users\austin.tracy\LearningHub\games\multiple_choice\history.csv")
    # Define choices
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 
    'w', 'x', 'y', 'z']
    random_letters, correct_letters, filename = set_up_a_round(df_letters)
    sound_played = False
    score = 0
    remaining_attempts = 3
    
    while True:
        if not sound_played:
            # Set the background color to black
            screen.fill((0, 0, 0))

            # Update the display
            pygame.display.flip()
            sound_played = True
            winsound.PlaySound(filename, winsound.SND_FILENAME)
        choices = [
            {"text": random_letters[0], "color": RED, "rect": pygame.Rect(0, 0, WIDTH // 2, HEIGHT // 2)},
            {"text": random_letters[1], "color": GREEN, "rect": pygame.Rect(WIDTH // 2, 0, WIDTH // 2, HEIGHT // 2)},
            {"text": random_letters[2], "color": BLUE, "rect": pygame.Rect(0, HEIGHT // 2, WIDTH // 2, HEIGHT // 2)},
            {"text": random_letters[3], "color": YELLOW, "rect": pygame.Rect(WIDTH // 2, HEIGHT // 2, WIDTH // 2, HEIGHT // 2)}
        ]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for choice in choices:
                        if choice["rect"].collidepoint(event.pos):
                            df_letters.loc[df_letters["Correct Answer"] == correct_letters[0],"Other Question Padding"] = 3
                            df_letters["Other Question Padding"] -=1
                            if choice["text"] in correct_letters:
                                # Update the streak for this letter
                                if df_letters.loc[df_letters["Correct Answer"] == correct_letters[0]]["Streak"].iloc[0] <= 0:
                                    df_letters.loc[df_letters["Correct Answer"] == correct_letters[0],"Streak"] = 1
                                else:
                                    df_letters.loc[df_letters["Correct Answer"] == correct_letters[0],"Streak"] += 1 
                                # Add the date for this being correct
                                df_letters.loc[df_letters["Correct Answer"] == correct_letters[0],"Last Correct Answer Date"] = str(datetime.now())
                                score += 1
                                celebration_screen(score)   
                            else:
                                # Update the streak for this letter
                                if df_letters.loc[df_letters["Correct Answer"] == correct_letters[0]]["Streak"].iloc[0] >= 0:
                                    df_letters.loc[df_letters["Correct Answer"] == correct_letters[0],"Streak"] = -1
                                else:
                                    df_letters.loc[df_letters["Correct Answer"] == correct_letters[0],"Streak"] -= 1 
                                show_incorrect_screen(3 - remaining_attempts,correct_letters,thumbs_down_image)
                                remaining_attempts -= 1
                                if remaining_attempts < 0:
                                    show_game_over_screen(score)
                                    score = 0
                                    remaining_attempts = 3
                            # Update the priority and Overall Score
                            df_letters.loc[df_letters["Correct Answer"] == correct_letters[0],"Priority"] -= df_letters.loc[df_letters["Correct Answer"] == correct_letters[0]]["Streak"]
                            df_letters.loc[df_letters["Correct Answer"] == correct_letters[0],"Overall Score"] += df_letters.loc[df_letters["Correct Answer"] == correct_letters[0]]["Streak"]
                            if df_letters.loc[df_letters["Correct Answer"] == correct_letters[0],"Priority"].any() > 10:
                                df_letters.loc[df_letters["Correct Answer"] == correct_letters[0],"Priority"] = 10
                            elif df_letters.loc[df_letters["Correct Answer"] == correct_letters[0],"Priority"].any() < 0:
                                df_letters.loc[df_letters["Correct Answer"] == correct_letters[0],"Priority"] = 0
                            df_letters.to_csv(r"C:\Users\austin.tracy\LearningHub\games\multiple_choice\history.csv",index=False)
                    random_letters, correct_letters, filename = set_up_a_round(df_letters)   

                    sound_played = False
        # Clear the screen
        screen.fill(WHITE)

        # Draw choices
        for choice in choices:
            pygame.draw.rect(screen, choice["color"], choice["rect"])
            text = font.render(choice["text"], True, BLACK)
            text_rect = text.get_rect(center=choice["rect"].center)
            screen.blit(text, text_rect)

        # Draw prompt box
        prompt_text = "Which letter?"
        prompt = prompt_font.render(prompt_text, True, BLACK)
        # Make this collidble to here the audio again.
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