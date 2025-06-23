import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 500
RADIUS = 20
GAP = 15
LETTERS_PER_ROW = 13
MAX_ATTEMPTS = 6
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Set up display
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman!")

# Fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 30)
WORD_FONT = pygame.font.SysFont('comicsans', 40)
TITLE_FONT = pygame.font.SysFont('comicsans', 50)

# Load Images
images = [pygame.image.load(f"hangman{i}.png") for i in range(7)]

class LetterButton:
    def __init__(self, x, y, letter):
        self.x = x
        self.y = y
        self.letter = letter
        self.visible = True

    def draw(self, surface):
        if self.visible:
            pygame.draw.circle(surface, BLACK, (self.x, self.y), RADIUS, 3)
            text = LETTER_FONT.render(self.letter, 1, BLACK)
            surface.blit(text, (self.x - text.get_width() / 2, self.y - text.get_height() / 2))

    def click(self, pos):
        if self.visible:
            distance = math.sqrt((self.x - pos[0]) ** 2 + (self.y - pos[1]) ** 2)
            return distance < RADIUS
        return False

class HangmanGame:
    def __init__(self):
        self.categories = {
            "Greetings": ["HELLO", "WELCOME", "BONJOUR", "GOODBYE"],
            "Animals": ["TIGER", "ELEPHANT", "GIRAFFE", "KANGAROO"],
            "Fruits": ["APPLE", "BANANA", "CHERRY", "MANGO"]
        }
        self.selected_category = None
        self.clock = pygame.time.Clock()
        self.running = True

    def select_category(self):
        while True:
            win.fill(WHITE)
            text = TITLE_FONT.render("Choose a Category", True, BLACK)
            win.blit(text, (WIDTH / 2 - text.get_width() / 2, 50))

            buttons = []
            for idx, category in enumerate(self.categories.keys()):
                rect = pygame.Rect(WIDTH / 2 - 100, 150 + idx * 80, 200, 50)
                pygame.draw.rect(win, GRAY, rect)
                cat_text = WORD_FONT.render(category, True, BLACK)
                win.blit(cat_text, (rect.centerx - cat_text.get_width() / 2, rect.centery - cat_text.get_height() / 2))
                buttons.append((rect, category))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for rect, category in buttons:
                        if rect.collidepoint(pos):
                            self.selected_category = category
                            return

    def reset(self):
        self.word = random.choice(self.categories[self.selected_category])
        self.guessed = []
        self.hangman_status = 0
        self.letter_buttons = self.create_letter_buttons()

    def create_letter_buttons(self):
        buttons = []
        startx = round((WIDTH - (RADIUS * 2 + GAP) * LETTERS_PER_ROW) / 2)
        starty = 400
        for i in range(26):
            x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % LETTERS_PER_ROW))
            y = starty + ((i // LETTERS_PER_ROW) * (GAP + RADIUS * 2))
            buttons.append(LetterButton(x, y, chr(65 + i)))
        return buttons

    def draw(self):
        win.fill(WHITE)
        text = TITLE_FONT.render("HANGMAN", 1, BLACK)
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

        display_word = " ".join([letter if letter in self.guessed else "_" for letter in self.word])
        text = WORD_FONT.render(display_word, 1, BLACK)
        win.blit(text, (380, 200))

        for button in self.letter_buttons:
            button.draw(win)

        win.blit(images[self.hangman_status], (150, 100))

        pygame.display.update()

    def display_end_screen(self, message):
        while True:
            win.fill(WHITE)
            text = WORD_FONT.render(message, 1, BLACK)
            win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - 120))

            play_again_rect = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 - 40, 200, 50)
            change_category_rect = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 + 30, 260, 50)
            quit_game_rect = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 + 100, 200, 50)

            # Draw buttons
            pygame.draw.rect(win, GRAY, play_again_rect)
            pygame.draw.rect(win, GRAY, change_category_rect)
            pygame.draw.rect(win, GRAY, quit_game_rect)

            # Render text
            play_again_text = WORD_FONT.render("Play Again", 1, BLACK)
            change_category_text = WORD_FONT.render("New Category", 1, BLACK)
            quit_game_text = WORD_FONT.render("Quit", 1, BLACK)

            # Blit text
            win.blit(play_again_text, (play_again_rect.centerx - play_again_text.get_width() / 2,
                                    play_again_rect.centery - play_again_text.get_height() / 2))
            win.blit(change_category_text, (change_category_rect.centerx - change_category_text.get_width() / 2,
                                            change_category_rect.centery - change_category_text.get_height() / 2))
            win.blit(quit_game_text, (quit_game_rect.centerx - quit_game_text.get_width() / 2,
                                    quit_game_rect.centery - quit_game_text.get_height() / 2))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if play_again_rect.collidepoint(pos):
                        return "restart"
                    elif change_category_rect.collidepoint(pos):
                        return "change_category"
                    elif quit_game_rect.collidepoint(pos):
                        pygame.quit()
                        exit()

    def run(self):
        self.select_category()
        self.reset()
        while self.running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for button in self.letter_buttons:
                        if button.click(pos):
                            button.visible = False
                            self.guessed.append(button.letter)
                            if button.letter not in self.word:
                                self.hangman_status += 1
                if event.type == pygame.KEYDOWN:
                    key = event.unicode.upper()
                    if 'A' <= key <= 'Z':  # Only letters
                        for button in self.letter_buttons:
                            if button.letter == key and button.visible:
                                button.visible = False
                                self.guessed.append(button.letter)
                                if button.letter not in self.word:
                                    self.hangman_status += 1


            self.draw()

            if all(letter in self.guessed for letter in self.word):
                pygame.time.delay(1000)
                result = self.display_end_screen("You WON!")
                if result == "restart":
                    self.reset()
                    continue
                elif result == "change_category":
                    self.select_category()
                    self.reset()
                    continue
                break

            if self.hangman_status == MAX_ATTEMPTS:
                pygame.time.delay(1000)
                result = self.display_end_screen(f"You LOST! The word was: {self.word}")
                if result == "restart":
                    self.reset()
                    continue
                elif result == "change_category":
                    self.select_category()
                    self.reset()
                    continue
                break


# Run game
game = HangmanGame()
game.run()
pygame.quit()
