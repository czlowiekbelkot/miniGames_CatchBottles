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

object_width, object_height = 15, 30


def draw_player(x, y):
    pygame.draw.rect(window, white, [x, y, player_width, player_height])
 

def draw_bottle(bottles):
    for bottle in bottles:
        pygame.draw.rect(window, green, bottle)
  

def draw_sopel(sopels):
    for sopel in sopels:
        pygame.draw.rect(window, red, sopel)


def collision_check(player, bottles, sopels):
    for bottle in bottles:
        if player.colliderect(bottle):
            bottles.remove(bottle)
            return True, True

    for sopel in sopels:
        if player.colliderect(sopel):
            sopels.remove(sopel)
            return True, False

    return False, False


def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    window.blit(text_surface, (x, y))


def game_loop():
    global player_x, player_speed
    clock = pygame.time.Clock()
    bottles = []
    sopels = []
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

        if random.randint(0, 100) < 2:
            sopels.append(pygame.Rect(random.randint(0, width - object_width), 0, object_width, object_height))

        for bottle in bottles:
            bottle.y += 10

        for sopel in sopels:
            sopel.y += 10

        caught, good_object = collision_check(pygame.Rect(player_x, player_y, player_width, player_height), bottles, sopels)

        if caught:
            if good_object:
                score += 0.1
            else:
                score -= 0.2
                score = max(score, 0)
                if score <= warning_threshold and not show_warning:
                    show_warning = True
                    warning_start_time = current_time

        window.fill((0, 0, 0))
        draw_player(player_x, player_y)
        draw_bottle(bottles)
        draw_sopel(sopels)

        score_text = "Alkohol we krwi: {:.1f}‰".format(score)
        draw_text(score_text, font, white, 10, 10)

        if show_warning and score <= warning_threshold:
            warning_text = "Rafałku! Trzeźwiejesz!"
            draw_text(warning_text, font, red, width // 2 - 100, height // 2)

            if current_time - warning_start_time >= warning_duration:
                show_warning = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()

        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_LEFT]:
            player_speed = -10
        elif keys_pressed[pygame.K_RIGHT]:
            player_speed = 10
        else:
            if pygame.K_RIGHT and pygame.K_LEFT not in keys_pressed:
                player_speed = 0

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    game_loop()
