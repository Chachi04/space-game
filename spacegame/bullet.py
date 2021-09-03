import pygame


class Bullet:
    def __init__(self, player):
        self.width = 10
        self.height = 5
        self.x = player.x + player.width if player.color == 'yellow' else player.x
        self.y = player.y + player.height//2 - 2
        self.vel = 7 if player.color == 'yellow' else -7
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw_bullet(self, win, color):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(win, color, self.rect)

    def handle_bullets(self):
        for bullet in self.bullets:
            bullet.x += bullet.vel
            # if player2.colliderect(bullet):
            #     pygame.event.post(pygame.event.Event(PLAYER2_HIT))
            #     player1.bullets.remove(bullet)

    def __repr__(self):
        return self.rect
