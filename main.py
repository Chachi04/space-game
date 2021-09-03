import pygame
import os

from spacegame import *
from spacegame import SpaceShip

pygame.font.init()
pygame.mixer.init()


HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)


bullet_fire_path = os.path.join('Assets', 'GunSilencer.wav')
bullet_hit_path = os.path.join('Assets', 'Grenade.wav')
BULLET_HIT_SOUND = pygame.mixer.Sound(bullet_hit_path)
BULLET_FIRE_SOUND = pygame.mixer.Sound(bullet_fire_path)
BULLET_FIRE_SOUND.set_volume(0.3)
BULLET_HIT_SOUND.set_volume(0.3)

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Game!")

FPS = 60

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

PLAYER1_HIT = pygame.USEREVENT + 1
PLAYER2_HIT = pygame.USEREVENT + 2

ship1_image_path = os.path.join('Assets', 'spaceship_yellow.png')
ship2_image_path = os.path.join('Assets', 'spaceship_red.png')
player1 = SpaceShip(os.path.join(ship1_image_path), 'yellow')
player2 = SpaceShip(os.path.join(ship2_image_path), 'red')

space_path = os.path.join('Assets', 'space.png')
SPACE = pygame.transform.scale(pygame.image.load(space_path), (WIDTH, HEIGHT))


def draw_window():
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    player1_health_text = HEALTH_FONT.render(
        f"Health: {player1.health}", 1, WHITE)
    player2_health_text = HEALTH_FONT.render(
        f"Health: {player2.health}", 1, WHITE)
    WIN.blit(player1_health_text, (10, 10))
    WIN.blit(player2_health_text,
             (WIDTH - player1_health_text.get_width() - 10, 10))

    player1.draw_spaceship(WIN)
    player2.draw_spaceship(WIN)
    for bullet in player1.bullets:
        bullet.draw_bullet(WIN, YELLOW)
    for bullet in player2.bullets:
        bullet.draw_bullet(WIN, RED)
    pygame.display.update()


def handle_bullets(player1, player2):
    for bullet in player1.bullets:
        bullet.x += bullet.vel
        if player2.colliderect(bullet.rect):
            pygame.event.post(pygame.event.Event(PLAYER2_HIT))
            player1.bullets.remove(bullet)
        elif bullet.x > WIDTH:
            player1.bullets.remove(bullet)
    for bullet in player2.bullets:
        bullet.x += bullet.vel
        if player1.colliderect(bullet.rect):
            pygame.event.post(pygame.event.Event(PLAYER1_HIT))
            player2.bullets.remove(bullet)
        elif bullet.x < 0:
            player2.bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))

    pygame.display.update()
    pygame.time.delay(5000)


def main():

    clock = pygame.time.Clock()

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(player1.bullets) < player1.max_bullets:
                    player1.fire()
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(player2.bullets) < player2.max_bullets:
                    player2.fire()
                    BULLET_FIRE_SOUND.play()
            if event.type == PLAYER1_HIT:
                player1.health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == PLAYER2_HIT:
                player2.health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ''
        if player1.health <= 0:
            winner_text = 'Red Wins!!!'
        if player2.health <= 0:
            winner_text = 'Yellow Wins!!!'
        if winner_text != '':
            draw_winner(winner_text)
            break

        pressed_keys = pygame.key.get_pressed()
        player1.spaceship_move(pressed_keys, BORDER)
        player2.spaceship_move(pressed_keys, BORDER)

        handle_bullets(player1, player2)

        draw_window()

    player1.reset()
    player2.reset()
    main()


if __name__ == '__main__':
    main()
