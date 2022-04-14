import pygame
import random
import os

WIDTH = 1280
HEIGHT = 720
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'game')

player_img = pygame.image.load(os.path.join(img_folder, 'white.jpg'))
player_img = pygame.transform.scale(player_img, (128, 128))

bullet_img = pygame.image.load(os.path.join(img_folder, 'bullet.png'))
bullet_img = pygame.transform.scale(bullet_img, (48, 48))

background = pygame.image.load(os.path.join(img_folder, 'rf.jpg'))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

meteor = pygame.image.load(os.path.join(img_folder, "ssr.jpg"))
meteor = pygame.transform.scale(meteor, (48, 48))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()

        self.radius = 200
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.shield = 100

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = 8
        if keystate[pygame.K_UP] or keystate[pygame.K_w]:
            self.speedy = -4
        if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
            self.speedy = 4

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < HEIGHT // 2:
            self.rect.top = HEIGHT // 2
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = meteor
        self.rect = self.image.get_rect()

        self.radius = self.rect.width * 0.85 // 2
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(2, 6)
        self.speedx = random.randrange(-3,  3)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.top > HEIGHT + 50 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-80, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -7

    def update(self):
        self.rect.y += self.speedy

        if self.rect.bottom < 0:
            self.kill()

def draw_text(surf, text, size, x ,y):
    font = pygame.font.Font(pygame.font.match_font('Arial'), size)

    color = WHITE
    if text > 10:
        color = RED
    if text > 40:
        color = GREEN

    text_surface = font.render(str(text), True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf, x ,y, pct):
    if pct < 0:
        pct = 0

    BAR_LENGTH = 100
    BAR_HEIGHT = 10

    fill = (pct / 100) * BAR_LENGTH

    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)

    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ЭТУ ИГРУ Я СДЕЛАЛ ОТВЕЧАЮ !!!!")

player = Player()
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

score = 0

for i in range(9):
    newmob()

running = True

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 1
        newmob()

    hits = pygame.sprite.spritecollide(player, mobs, True)
    for hit in hits:
        player.shield -= hit.radius * 2
        newmob()

        if player.shield <= 0:
           running = False

    screen.blit(background, background.get_rect())
    all_sprites.draw(screen)

    draw_text(screen, score, 64, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    pygame.display.flip()

pygame.quit()
