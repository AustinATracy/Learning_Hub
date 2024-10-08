from datetime import datetime
import pygame
import random
from re import sub
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
    correct_answer = df_letters_condensed.loc[correct_answer_index]["Correct Answer"]
    df_letters.drop("Total Priority",axis=1)
    return letters, correct_answer

def set_up_a_round(df_letters):
        letters, correct_letter = get_letters(df_letters)
        disallowed_letters = []
        if correct_letter == "c":
            if random.random() > 0:
                audio_letter = "k"
                correct_letter_rep = random.choices(["c(a)","c(o)","c(u)","c(k)","c"],[1,1,1,5,20],k=1)[0]
                disallowed_letters = ["k","q"]
            else:
                audio_letter = "s"
                correct_letter_rep = random.choice(["c(e)","c(i)"])[0]
                disallowed_letters = ["s"]
        else:
            correct_letter_rep = correct_letter
        
        if correct_letter == "q":
            audio_letter = "k"
            disallowed_letters = ["c","k"]
        elif correct_letter == "k":
            audio_letter = "k"
            disallowed_letters = ["c","q"]
        elif correct_letter == "s":
            audio_letter = "s"
            disallowed_letters = ["c"]
        elif correct_letter == "n":
            audio_letter = "n"
            disallowed_letters = ["m"]
        elif correct_letter == "m":
            audio_letter = "m"
            disallowed_letters = ["n"]
        else:
            audio_letter = correct_letter
        letters = list(set(letters).difference(disallowed_letters).difference(correct_letter))
        random_letters = [correct_letter_rep]
        for i in range(3):
            random_selection = random.choice(letters)
            random_letters.append(random_selection)
            letters.remove(random_selection)
        random.shuffle(random_letters)
        filename = f'{audio_letter}.wav'
        import pyautogui
        pyautogui.alert(correct_letter)
        
        pyautogui.alert(correct_letter_rep)
        return random_letters, correct_letter, filename, correct_letter_rep
    

# Main game loop
def main():
    df_letters = pd.read_csv(r"C:\Users\austin.tracy\LearningHub\games\multiple_choice\history.csv")
    # Define choices
    random_letters, correct_letter, filename, correct_letter_rep = set_up_a_round(df_letters)
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
                            df_letters.loc[df_letters["Correct Answer"] == correct_letter,"Other Question Padding"] = 3
                            df_letters["Other Question Padding"] -=1
                            chosen_sequence = sub(r"\(.*\)","",choice["text"])
                            if chosen_sequence == correct_letter:
                                # Update the streak for this letter
                                if df_letters.loc[df_letters["Correct Answer"] == correct_letter]["Streak"].iloc[0] <= 0:
                                    df_letters.loc[df_letters["Correct Answer"] == correct_letter,"Streak"] = 1
                                else:
                                    df_letters.loc[df_letters["Correct Answer"] == correct_letter,"Streak"] += 1 
                                # Add the date for this being correct
                                df_letters.loc[df_letters["Correct Answer"] == correct_letter,"Last Correct Answer Date"] = str(datetime.now())
                                score += 1
                                celebration_screen(score)   
                            else:
                                # Update the streak for this letter
                                if df_letters.loc[df_letters["Correct Answer"] == correct_letter]["Streak"].iloc[0] >= 0:
                                    df_letters.loc[df_letters["Correct Answer"] == correct_letter,"Streak"] = -1
                                else:
                                    df_letters.loc[df_letters["Correct Answer"] == correct_letter,"Streak"] -= 1 
                                show_incorrect_screen(3 - remaining_attempts,correct_letter,thumbs_down_image)
                                remaining_attempts -= 1
                                if remaining_attempts < 0:
                                    show_game_over_screen(score)
                                    score = 0
                                    remaining_attempts = 3
                            # Update the priority and Overall Score
                            df_letters.loc[df_letters["Correct Answer"] == correct_letter,"Priority"] -= df_letters.loc[df_letters["Correct Answer"] == correct_letter]["Streak"]
                            df_letters.loc[df_letters["Correct Answer"] == correct_letter,"Overall Score"] += df_letters.loc[df_letters["Correct Answer"] == correct_letter]["Streak"]
                            if df_letters.loc[df_letters["Correct Answer"] == correct_letter,"Priority"].iloc[0] > 10:
                                df_letters.loc[df_letters["Correct Answer"] == correct_letter,"Priority"] = 10
                            elif df_letters.loc[df_letters["Correct Answer"] == correct_letter,"Priority"].iloc[0] < 0:
                                df_letters.loc[df_letters["Correct Answer"] == correct_letter,"Priority"] = 0
                            df_letters.to_csv(r"C:\Users\austin.tracy\LearningHub\games\multiple_choice\history.csv",index=False)
                    random_letters, correct_letter, filename, correct_letter_rep = set_up_a_round(df_letters)   

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