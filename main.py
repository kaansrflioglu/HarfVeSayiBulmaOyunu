import pygame
import random
import sys

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Düşen Karakterler Oyunu")

pygame.mixer.music.load("requirements/music.mp3")
pygame.mixer.music.play(-1)

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 128, 0)
turquoise = (64, 224, 208)

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 74)

letters = []
letter_index = 0
letter = None
letter_x = 0
letter_y = 0
letter_speed_y = 0
letter_speed_x = 0
score = 0
game_over = False

include_letters = False
include_numbers = False

speed_options = [
    {"speed": 10, "text": "Yavaş"},
    {"speed": 25, "text": "Normal"},
    {"speed": 50, "text": "Hızlı"},
    {"speed": 100, "text": "Çok Hızlı"}
]
selected_speed = speed_options[0]["speed"]

theme_options = [
    {"name": "Tema 1", "file": "requirements/background1.jpg"},
    {"name": "Tema 2", "file": "requirements/background2.jpg"},
    {"name": "Tema 3", "file": "requirements/background3.png"},
    {"name": "Tema 4", "file": "requirements/background4.jpg"},
    {"name": "Tema 5", "file": "requirements/background5.png"}
]
selected_theme = theme_options[0]["file"]

clock = pygame.time.Clock()

background_image = None
bubble_width = 100
bubble_height = 100
bubble_image = pygame.image.load("requirements/bubble.png")
bubble_image = pygame.transform.scale(bubble_image,
                                      (int(bubble_image.get_width() * bubble_width/100),
                                       int(bubble_image.get_height() * (bubble_height/100))))

pygame.mixer.init()
correct_sound = pygame.mixer.Sound("requirements/correct.mp3")


def reset_game():
    global letters, letter_index, letter, letter_x, letter_y, letter_speed_y, letter_speed_x, score, game_over, include_letters, include_numbers
    letters = []
    letter_index = 0
    letter = None
    letter_x = 0
    letter_y = 0
    letter_speed_y = 0
    letter_speed_x = 0
    score = 0
    game_over = False
    include_letters = False
    include_numbers = False
    start_screen()


def pause_screen():
    paused = True
    while paused:
        screen.fill(turquoise)
        paused_text = big_font.render("Oyun Durdu", True, white)
        screen.blit(paused_text, (screen_width // 2 - 150, screen_height // 2 - 150))

        devam_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 80, 200, 50)
        pygame.draw.rect(screen, green, devam_button_rect)
        screen.blit(font.render("Devam Et", True, black), (devam_button_rect.x + 42, devam_button_rect.y + 10))

        re_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 20, 200, 50)
        pygame.draw.rect(screen, green, re_button_rect)
        screen.blit(font.render("Tekrar Oyna", True, black), (re_button_rect.x + 25, re_button_rect.y + 10))

        pygame.display.flip()
        clock.tick(60)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    paused = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                if devam_button_rect.collidepoint(e.pos):
                    paused = False
                elif re_button_rect.collidepoint(e.pos):
                    reset_game()
                    paused = False


def start_screen():
    global include_letters, include_numbers, selected_speed
    while True:
        screen.fill(turquoise)

        title_text = big_font.render("Düşen Karakterler Oyunu", True, white)
        screen.blit(title_text, (screen_width // 2 - 315, 100))

        render_checkbox("Harfler (A-Z)", 180, 250, include_letters)
        render_checkbox("Sayılar (0-9)", 480, 250, include_numbers)

        speed_text = font.render("Hız Seçeneği:", True, white)
        screen.blit(speed_text, (screen_width / 2 - 70, 300))
        for i, option in enumerate(speed_options):
            checkbox_x = 120 + (i * 150)
            checkbox_rect = pygame.Rect(checkbox_x, 350, 20, 20)
            pygame.draw.rect(screen, white, checkbox_rect, 2)
            if option["speed"] == selected_speed:
                pygame.draw.rect(screen, blue, checkbox_rect.inflate(-4, -4))
            screen.blit(font.render(option["text"], True, white), (checkbox_x + 25, 347))
            if checkbox_rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    selected_speed = option["speed"]

        basla_button_rect = pygame.Rect(screen_width // 2 - 50, 400, 100, 50)
        if include_letters or include_numbers:
            pygame.draw.rect(screen, blue, basla_button_rect)
            button_color = white
        else:
            pygame.draw.rect(screen, (100, 100, 100), basla_button_rect)
            button_color = (150, 150, 150)

        screen.blit(font.render("Başla", True, button_color), (screen_width // 2 - 33, 412))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if render_checkbox("Harfler (A-Z)", 180, 250, include_letters, True):
                    include_letters = not include_letters
                if render_checkbox("Sayılar (0-9)", 480, 250, include_numbers, True):
                    include_numbers = not include_numbers
                if basla_button_rect.collidepoint(e.pos) and (include_letters or include_numbers):
                    theme_selection_screen()
                    return

        pygame.display.flip()
        clock.tick(60)


def render_checkbox(t, x, y, checked, click_check=False):
    rect = pygame.Rect(x, y, 20, 20)
    pygame.draw.rect(screen, white, rect, 2)
    if checked:
        pygame.draw.rect(screen, blue, rect.inflate(-4, -4))
    screen.blit(font.render(t, True, white), (x + 30, y - 5))
    if click_check and rect.collidepoint(pygame.mouse.get_pos()):
        return True


def theme_selection_screen():
    global selected_theme
    while True:
        screen.fill(turquoise)

        title_text = big_font.render("Tema Seçimi", True, white)
        screen.blit(title_text, (screen_width // 2 - 100, 100))

        for i, theme in enumerate(theme_options):
            checkbox_x = 150
            checkbox_y = 200 + i * 60
            checkbox_rect = pygame.Rect(checkbox_x, checkbox_y, 20, 20)
            pygame.draw.rect(screen, white, checkbox_rect, 2)
            if theme["file"] == selected_theme:
                pygame.draw.rect(screen, blue, checkbox_rect.inflate(-4, -4))
            screen.blit(font.render(theme["name"], True, white), (checkbox_x + 30, checkbox_y - 5))
            if checkbox_rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    selected_theme = theme["file"]

        basla_button_rect = pygame.Rect(screen_width // 2 - 50, 400, 100, 50)
        pygame.draw.rect(screen, blue, basla_button_rect)
        screen.blit(font.render("Başla", True, white), (screen_width // 2 - 33, 412))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if basla_button_rect.collidepoint(e.pos):
                    load_background_image()
                    setup_game()
                    return

        pygame.display.flip()
        clock.tick(60)


def load_background_image():
    global background_image
    background_image = pygame.image.load(selected_theme)
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))


def setup_game():
    global letters, letter_speed_y, letter_speed_x, letter_index, letter, letter_x, letter_y

    if include_letters:
        letters.extend([chr(i) for i in range(65, 91)])
    if include_numbers:
        letters.extend([str(i) for i in range(0, 10)])

    if not letters:
        raise ValueError("Harfler ve sayılar listesi boş!")

    random.shuffle(letters)
    letter_speed_y = selected_speed / 10
    letter_speed_x = random.choice([-1, 1]) * selected_speed / 20
    letter_index = 0
    letter = letters[letter_index]
    letter_x = screen_width // 2
    letter_y = 0


start_screen()

running = True
correct_guess = False
correct_guess_time = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.unicode.upper() == letter:
                    score += 1
                    correct_guess = True
                    correct_guess_time = pygame.time.get_ticks()
                    correct_sound.play()
                elif event.key == pygame.K_ESCAPE:
                    pause_screen()

        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            tekrar_button_rect = pygame.Rect(screen_width // 2 - 95, screen_height // 2 + 10, 200, 50)
            if tekrar_button_rect.collidepoint(event.pos):
                reset_game()
                game_over = False

    if not game_over:
        if correct_guess:
            correct_guess = False
            letter_index += 1
            if letter_index < len(letters):
                letter = letters[letter_index]
                letter_x = screen_width // 2
                letter_y = 0
                letter_speed_x = random.choice([-1, 1]) * selected_speed / 20
            else:
                game_over = True
        else:
            letter_y += letter_speed_y
            letter_x += letter_speed_x

            if letter_y > screen_height:
                letter_index += 1
                if letter_index < len(letters):
                    letter = letters[letter_index]
                    letter_x = screen_width // 2
                    letter_y = 0
                    letter_speed_x = random.choice([-1, 1]) * selected_speed / 20
                else:
                    game_over = True

            if letter_x <= 0 or letter_x >= screen_width:
                letter_speed_x *= -1

            screen.blit(background_image, (0, 0))

            bubble_x = letter_x - bubble_image.get_width() // 2
            bubble_y = letter_y - bubble_image.get_height() // 2
            screen.blit(bubble_image, (bubble_x, bubble_y))

            text = big_font.render(letter, True, white)
            text_x = letter_x - text.get_width() // 2
            text_y = letter_y - text.get_height() // 2
            screen.blit(text, (text_x, text_y))

        score_text = font.render("Doğru Sayısı: " + str(score), True, white)
        screen.blit(score_text, (10, 10))
    else:
        game_over_text = big_font.render("Oyun Bitti", True, white)
        screen.blit(game_over_text, (screen_width // 2 - 125, screen_height // 2 - 100))

        final_score_text = font.render("Doğru Sayısı: " + str(score), True, white)
        screen.blit(final_score_text, (screen_width // 2 - 125, screen_height // 2 - 40))

        tekrar_button_rect = pygame.Rect(screen_width // 2 - 95, screen_height // 2 + 10, 200, 50)
        pygame.draw.rect(screen, green, tekrar_button_rect)
        screen.blit(font.render("Tekrar Oyna", True, black), (tekrar_button_rect.x + 26, tekrar_button_rect.y + 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
