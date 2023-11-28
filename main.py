import pygame
import sys
import random

pygame.init()

### Display settings ###
width = 600 
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Catch Bottle")

### Colors ###
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

### Player set ###
player_width, player_height = 30, 55
player_x = (width - player_width) / 2
player_y = height - player_height
player_speed = 0
 
### Objects ###
object_width, object_height = 15, 30
  
### Draw player ###
def draw_player(x, y):
    pygame.draw.rect(window, white, [x, y, player_width, player_height])
 
### Draw bottle ###
def draw_bottle(bottles):
    for bottle in bottles:
        pygame.draw.rect(window, green, bottle)
  
### Draw sopel ###
def draw_sopel(sopels):
    for sopel in sopels:
        pygame.draw.rect(window, red, sopel)

### Collision check ###
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_speed = -10 
                elif event.key == pygame.K_RIGHT:
                    player_speed = 10

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_speed = 0

        ### Update player position ###
        player_x += player_speed

        ### Limit player to screen border ###
        player_x = max(0, min(player_x, width - player_width))

        ### Add a new bottle ###
        if random.randint(0, 100) < 1: ### Change if you want to more bottles
            bottles.append(pygame.Rect(random.randint(0, width - object_width), 0, object_width, object_height))

        ### Add a new sopel ###
        if random.randint(0, 100) < 2: ### Change if you want to more sopels
            sopels.append(pygame.Rect(random.randint(0, width - object_width), 0, object_width, object_height))

        ### Speed objects ###
        for bottle in bottles:
            bottle.y += 10

        for sopel in sopels:
            sopel.y += 10

        ### Check collision ###
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
       
        ### Draw objects ###
        window.fill((0, 0, 0))
        draw_player(player_x, player_y)
        draw_bottle(bottles)
        draw_sopel(sopels)

        ### Display score ###
        score_text = "Alkohol we krwi: {:.1f}‰".format(score)
        draw_text(score_text, font, white, 10, 10)

        ### Display warning ###
        if show_warning and score <= warning_threshold:
            warning_text = "Rafałku! Trzeźwiejesz!"
            draw_text(warning_text, font, red, width // 2 - 100, height // 2)

            if current_time - warning_start_time >= warning_duration:
                show_warning = False

        pygame.display.flip()
        clock.tick(60)

### Start the game loop
game_loop()
