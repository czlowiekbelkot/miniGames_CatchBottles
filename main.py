import pygame
import sys
import random

pygame.init()

width = 600
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Catch Bottle")

white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

player_width, player_height = 30, 55
player_x = (width - player_width) / 2
player_y = height - player_height
player_speed = 0
last_key = None
player_image = pygame.image.load('player.jpg')

object_width, object_height = 15, 55
bottle_image = pygame.image.load('bottle.jpg')
sopel_image = pygame.image.load('sopel.jpg')

esperal_width, esperal_height = 250, 120
esperal_image = pygame.image.load('esperal.png').convert_alpha()


def draw_player(x, y):
    window.blit(player_image, (x, y))


def draw_bottle(bottles):
    for bottle in bottles:
        window.blit(bottle_image, bottle)


def draw_sopel(sopels):
    for sopel in sopels:
        window.blit(sopel_image, sopel)


def draw_esperal(esperals):
    for esperal in esperals:
        window.blit(esperal_image, esperal)


def collision_check(player, bottles, sopels, esperals):
    for bottle in bottles:
        if player.colliderect(bottle):
            bottles.remove(bottle)
            return True, True, False

    for sopel in sopels:
        if player.colliderect(sopel):
            sopels.remove(sopel)
            return True, False, False

    for esperal in esperals:
        if player.colliderect(esperal):
            return True, True, True

    return False, False, False


def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    window.blit(text_surface, (x, y))


def game_over_screen(font):
    draw_text("Game Over", font, red, width // 2 - 65, height // 2 - 100)
    draw_text("Press Enter to Play Again", font, white, width // 2 - 155, height // 2 - 50)

    pygame.display.flip()

    waiting_for_enter = True
    while waiting_for_enter:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting_for_enter = False
    return True


def game_loop():
    global player_x, player_speed, last_key
    clock = pygame.time.Clock()
    bottles = []
    sopels = []
    rozbitki = []
    esperals = []
    score = 0
    show_warning = False
    warning_threshold = 1.2
    warning_start_time = 500
    warning_duration = 3000
    font = pygame.font.Font(None, 36)

    while True:
        current_time = pygame.time.get_ticks()

        # Update player position
        player_x += player_speed

        # Limit player to screen border
        player_x = max(0, min(player_x, width - player_width))

        if random.randint(0, 100) < 1:
            bottles.append(pygame.Rect(random.randint(0, width - object_width), 0, object_width, object_height))

        if random.randint(0, 100) < 5:
            sopels.append(pygame.Rect(random.randint(0, width - object_width), 0, object_width, object_height))

        if random.random() < 0.0001:
            esperals.append(pygame.Rect(random.randint(0, width - esperal_width), 0, esperal_width, esperal_height))

        for bottle in bottles:
            bottle.y += 8
            if bottle.y > height:
                rozbitki.append(bottle)
                bottles.remove(bottle)

        for sopel in sopels:
            sopel.y += 10

        for esperal in esperals:
            esperal.y += 12

        caught, good_object, game_over = collision_check(pygame.Rect(player_x, player_y, player_width, player_height), bottles,
                                              sopels, esperals)

        if caught:
            if good_object:
                score += 0.1
            else:
                score -= 1
                if score <= warning_threshold and not show_warning:
                    show_warning = True
                    warning_start_time = current_time

        if score < 0 and not game_over:
            game_over = True
            show_warning = False

        if game_over:
            if game_over_screen(font):
                player_x = (width - player_width) / 2
                player_speed = 0
                score = 0
                bottles.clear()
                sopels.clear()
                rozbitki.clear()

        window.fill((0, 0, 0))
        draw_player(player_x, player_y)
        draw_bottle(bottles)
        draw_sopel(sopels)
        draw_esperal(esperals)

        score_text = "Alkohol we krwi: {:.1f}‰".format(score)
        draw_text(score_text, font, white, 10, 10)
        missed_text = "Rozbite buteleczki: {:2d}".format(len(rozbitki))
        draw_text(missed_text, font, red, width - 270, 10)

        if show_warning and score <= warning_threshold:
            warning_text = "Rafałku! Trzeźwiejesz!"
            draw_text(warning_text, font, red, width // 2 - 135, height // 2)

            if current_time - warning_start_time >= warning_duration:
                show_warning = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    last_key = "left"
                if event.key == pygame.K_RIGHT:
                    last_key = "right"

        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_LEFT]:
            if last_key == "right" and keys_pressed[pygame.K_RIGHT]:
                player_speed = 10
            else:
                player_speed = -10
        elif keys_pressed[pygame.K_RIGHT]:
            player_speed = 10
        else:
            player_speed = 0

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    game_loop()
