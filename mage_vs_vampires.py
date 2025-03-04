import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Mage vs. Vampires")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
# Font
font_name = 'Arial'
font_size = 36

# Load pixel art assets (replace with your own)
mage_img = pygame.Surface((32, 32))
mage_img.fill(GREEN)
vampire_img = pygame.Surface((32, 32))
vampire_img.fill(RED)
fireball_img = pygame.Surface((16, 16))
fireball_img.fill((255, 165, 0))  # Orange for fireballmage_img = pygame.image.load('mage.png')
mage_img = pygame.image.load('mage.png')
vampire_img = pygame.image.load('vampire.png')
fireball_img = pygame.image.load('fireball.png')
score = 0

# Player (Mage)
class Mage(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = mage_img
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT // 2
        self.speed = 5
        self.health = 100
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < HEIGHT - self.rect.height:
            self.rect.y += self.speed

    def shoot(self):
        fireball = Fireball(self.rect.centerx, self.rect.centery)
        all_sprites.add(fireball)
        fireballs.add(fireball)

# Enemy (Vampire)
class Vampire(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = vampire_img
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + random.randint(50, 200)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.speed = random.randint(2, 4)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# Projectile (Fireball)
class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = fireball_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 8

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.kill()

# Sprite groups
all_sprites = pygame.sprite.Group()
vampires = pygame.sprite.Group()
fireballs = pygame.sprite.Group()

# Create player
mage = Mage()
all_sprites.add(mage)

# Game loop
running = True
clock = pygame.time.Clock()
spawn_timer = 0
spawn_interval = 1000  # Spawn every 1 second

while running:
    clock.tick(60)  # 60 frames per second

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            mage.shoot()

    # Spawn vampires
    spawn_timer += clock.get_time()
    if spawn_timer > spawn_interval:
        vampire = Vampire()
        all_sprites.add(vampire)
        vampires.add(vampire)
        spawn_timer = 0

    # Update sprites
    all_sprites.update()

    # Collision detection
    hits = pygame.sprite.groupcollide(vampires, fireballs, True, True)
    for hit in hits:
        # Vampire hit by fireball
        score += 10
          # Add score or effects here

    hits = pygame.sprite.spritecollide(mage, vampires, True)
    for hit in hits:
        mage.health -= 20
        if mage.health <= 0:
            running = False #game over

    # Draw everything
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Draw health bar
    pygame.draw.rect(screen, RED, (10, 10, mage.health, 10))
    font = pygame.font.SysFont(font_name, font_size)
    text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, (WIDTH // 2 - 50, 10))
    pygame.display.flip()

pygame.quit()