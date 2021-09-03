import pygame
from spacegame.bullet import Bullet


class SpaceShip:
    def __init__(self, image_path, color):
        self.health = 10
        self.height = 55
        self.width = 44
        self.size = (self.width, self.height)
        self.color = color
        self.rotation = 90 if self.color == 'yellow' else -90
        self.image = pygame.image.load(image_path)
        self.ship = pygame.transform.rotate(pygame.transform.scale(
            self.image, (self.height, self.width)), self.rotation)
        self.x = 100 if self.color == 'yellow' else 700
        self.y = 250
        self.up = pygame.K_w if color == 'yellow' else pygame.K_UP
        self.down = pygame.K_s if color == 'yellow' else pygame.K_DOWN
        self.left = pygame.K_a if color == 'yellow' else pygame.K_LEFT
        self.right = pygame.K_d if color == 'yellow' else pygame.K_RIGHT
        self.vel = 5
        self.bullets = []
        self.max_bullets = 3

    def draw_spaceship(self, win):
        self.pos = self.x, self.y
        win.blit(self.ship, self.pos)

    def fire(self):
        bullet = Bullet(self)
        self.bullets.append(bullet)

    def spaceship_move(self, pressed_keys, border):
        if self.color == 'yellow':
            right_border_limit = border.x - self.width
            left_border_limit = 0
        else:
            right_border_limit = 900 - self.width
            left_border_limit = border.x+border.width
        if pressed_keys[self.left] and self.x - self.vel > left_border_limit:  # LEFT
            self.x -= self.vel
        if pressed_keys[self.right] and self.x + self.vel < right_border_limit:  # RIGHT
            self.x += self.vel
        if pressed_keys[self.up] and self.y - self.vel > 0:  # UP
            self.y -= self.vel
        if pressed_keys[self.down] and self.y + self.vel + self.height < 500:  # DOWN
            self.y += self.vel

    def colliderect(self, bullet):
        return pygame.Rect(self.x, self.y, self.width, self.height).colliderect(bullet)

    def reset(self):
        self.health = 10
        self.x = 100 if self.color == 'yellow' else 700
        self.y = 250
        self.bullets = []
        self.max_bullets = 3
