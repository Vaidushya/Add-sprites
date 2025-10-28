import pygame
import random
import math

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
MOVEMENT_SPEED = 5
FONT_SIZE = 72
SPRITE2_SPEED = 3
AVOID_RADIUS = 100

# Initialize Pygame
pygame.init()

# try for bg
try:
    background_image = pygame.transform.scale(
        pygame.image.load("bg.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
except:
    background_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_image.fill(pygame.Color("lightblue"))

# Load font
font = pygame.font.SysFont("Times New Roman", FONT_SIZE)

class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, height, width):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def move(self, x_change, y_change):
        # Keep inside window
        self.rect.x = max(min(self.rect.x + x_change, SCREEN_WIDTH - self.rect.width), 0)
        self.rect.y = max(min(self.rect.y + y_change, SCREEN_HEIGHT - self.rect.height), 0)


class BouncingSprite(Sprite):
    def __init__(self, color, height, width):
        super().__init__(color, height, width)
        self.vx = random.choice([-1, 1]) * SPRITE2_SPEED
        self.vy = random.choice([-1, 1]) * SPRITE2_SPEED

    def update(self, other):
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.vx = -self.vx
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.vy = -self.vy

        dx = self.rect.centerx - other.rect.centerx
        dy = self.rect.centery - other.rect.centery
        dist = math.hypot(dx, dy)

        if dist < AVOID_RADIUS and dist != 0:
            dx /= dist
            dy /= dist
            self.rect.x += dx * SPRITE2_SPEED
            self.rect.y += dy * SPRITE2_SPEED

        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))


# screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the Reddy🟥")
all_sprites = pygame.sprite.Group()

# making sprites
sprite1 = Sprite(pygame.Color('dodgerblue'), 20, 30)
sprite1.rect.x = random.randint(0, SCREEN_WIDTH - sprite1.rect.width)
sprite1.rect.y = random.randint(0, SCREEN_HEIGHT - sprite1.rect.height)

sprite2 = BouncingSprite(pygame.Color('red'), 20, 30)
sprite2.rect.x = random.randint(0, SCREEN_WIDTH - sprite2.rect.width)
sprite2.rect.y = random.randint(0, SCREEN_HEIGHT - sprite2.rect.height)

all_sprites.add(sprite1, sprite2)

# Game loop variables
running, won = True, False
clock = pygame.time.Clock()

# main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_x):
            running = False

    if not won:
        keys = pygame.key.get_pressed()
        x_change = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * MOVEMENT_SPEED
        y_change = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * MOVEMENT_SPEED
        sprite1.move(x_change, y_change)
        sprite2.update(sprite1)

        if sprite1.rect.colliderect(sprite2.rect):
            all_sprites.remove(sprite2)
            won = True

    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)

    if won:
        win_text = font.render("You win!", True, pygame.Color('black'))
        screen.blit(
            win_text,
            ((SCREEN_WIDTH - win_text.get_width()) // 2,
             (SCREEN_HEIGHT - win_text.get_height()) // 2)
        )

    pygame.display.flip()
    clock.tick(90)

pygame.quit()
