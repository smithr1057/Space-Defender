import pygame
import random
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# Calculates the game timer and outputs
def game_timer():
    ticks = pygame.time.get_ticks()
    seconds = int(ticks / 1000 % 60)
    minutes = int(ticks / 60000 % 24)
    return f'{minutes:02d}:{seconds:02d}'


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("Images/Bat.png").convert_alpha()
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.move_speed = 5
        self.last_shot = pygame.time.get_ticks()
        self.shoot_cooldown = 250  # milliseconds

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.move_speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.move_speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.move_speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.move_speed, 0)

        # Keep player on the screen
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(SCREEN_WIDTH, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(SCREEN_HEIGHT, self.rect.bottom)

    def shoot(self, shot):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot >= self.shoot_cooldown:
            self.last_shot = current_time
            if shot % 2 == 0:
                return PlayerBullet(self.rect.topright)
            else:
                return PlayerBullet(self.rect.topleft)
        return None


class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(PlayerBullet, self).__init__()
        self.surf = pygame.image.load("Images/player_bullet_fixed.png").convert_alpha()
        original_width, original_height = self.surf.get_size()
        desired_width = 30
        desired_height = int(original_height * (desired_width / original_width))
        self.surf = pygame.transform.smoothscale(self.surf, (desired_width, desired_height))
        self.rect = self.surf.get_rect(center=pos)
        self.speed = -10  # Bullet speed

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom < 0:
            self.kill()


class Astroid(pygame.sprite.Sprite):
    def __init__(self):
        super(Astroid, self).__init__()
        self.surf = pygame.image.load("Images/asteroid.png").convert_alpha()
        original_width, original_height = self.surf.get_size()
        desired_width = random.randint(30, 70)
        desired_height = int(original_height * (desired_width / original_width))
        self.surf = pygame.transform.smoothscale(self.surf, (desired_width, desired_height))
        self.rect = self.surf.get_rect(center=(random.randint(0, SCREEN_WIDTH), random.randint(-100, -20)))
        self.speed = random.randint(2, 15)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Aliens(pygame.sprite.Sprite):
    def __init__(self):
        super(Aliens, self).__init__()
        self.surf = pygame.image.load("Images/aliens.png").convert_alpha()
        original_width, original_height = self.surf.get_size()
        desired_width = 50
        desired_height = int(original_height * (desired_width / original_width))
        self.surf = pygame.transform.smoothscale(self.surf, (desired_width, desired_height))
        self.rect = self.surf.get_rect(center=(random.randint(0, SCREEN_WIDTH), 50))
        self.move_speed = random.choice([5, -5])
        self.shoot_delay = random.randint(500, 2000)  # milliseconds
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.rect.move_ip(self.move_speed, 0)
        if self.rect.left < 0:
            self.move_speed = 5
        if self.rect.right > SCREEN_WIDTH:
            self.move_speed = -5

        # Handle shooting
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            self.last_shot = current_time
            new_bullet = self.shoot()
            if new_bullet:
                alien_bullets.add(new_bullet)
                all_sprites.add(new_bullet)

    def shoot(self):
        shot = random.randint(0, 1)
        if shot == 0:
            return AlienBullet(self.rect.bottomleft)
        else:
            return AlienBullet(self.rect.bottomright)


class AlienBullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(AlienBullet, self).__init__()
        self.surf = pygame.image.load("Images/alien_bullet_fixed.png").convert_alpha()
        original_width, original_height = self.surf.get_size()
        desired_width = 30
        desired_height = int(original_height * (desired_width / original_width))
        self.surf = pygame.transform.smoothscale(self.surf, (desired_width, desired_height))
        self.rect = self.surf.get_rect(center=pos)
        self.speed = 10  # Bullet speed

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# Initialize pygame
pygame.init()

# Set up the clock for a decent frame rate
clock = pygame.time.Clock()

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load the background image
background = pygame.image.load("background.jpg").convert()

# Define the RGB value for white, green, blue, and black color
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)

font = pygame.font.Font('freesansbold.ttf', 32)

# Instantiate player
player = Player()

# Create groups to hold enemy sprites and all sprites
enemies = pygame.sprite.Group()
aliens = pygame.sprite.Group()
astroids = pygame.sprite.Group()  # Ensure this group is correctly named and used
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Create groups to hold bullet sprites
bullets = pygame.sprite.Group()
alien_bullets = pygame.sprite.Group()

# Create a custom event for adding a new astroid
ADDASTROID = pygame.USEREVENT + 1
pygame.time.set_timer(ADDASTROID, random.randint(500, 2000))

# Create a custom event for adding a new Alien
ADDALIEN = pygame.USEREVENT + 2
pygame.time.set_timer(ADDALIEN, random.randint(1000, 3000))

shots = 0
SCORE = 0

# Variable to keep the main loop running
running = True

# Main loop
while running:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:  # Shoot bullet when space bar is pressed
                new_bullet = player.shoot(shots)
                if new_bullet is not None:
                    bullets.add(new_bullet)
                    all_sprites.add(new_bullet)
                    shots += 1

        elif event.type == QUIT:
            running = False

        elif event.type == ADDASTROID:
            new_enemy = Astroid()
            astroids.add(new_enemy)
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ADDALIEN:
            new_enemy = Aliens()
            aliens.add(new_enemy)
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    keys_pressed = pygame.key.get_pressed()
    player.update(keys_pressed)
    enemies.update()
    bullets.update()
    alien_bullets.update()

    # Fill the screen with the background image
    screen.blit(background, (0, 0))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check for collisions between bullets and asteroids
    for bullet in bullets:
        hit_astroids = pygame.sprite.spritecollide(bullet, astroids, True)
        hit_enemies = pygame.sprite.spritecollide(bullet, aliens, True)

        if hit_astroids:
            SCORE += 1
            bullet.kill()
        if hit_enemies:
            SCORE += 5
            bullet.kill()

    # Check for collisions between player and enemy bullets
    if pygame.sprite.spritecollideany(player, alien_bullets):
        player.kill()
        running = False

    # Check for collisions between player and enemies
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False

    # Convert SCORE to a string
    SCORE_STR = str(SCORE)

    # Create a text surface object, on which text is drawn on it.
    text = font.render(f"{SCORE}", True, white)

    textRect = text.get_rect()

    # Multiply 10 by the length of the score
    score_x_position = 10 * len(SCORE_STR)

    textRect.center = (score_x_position, SCREEN_HEIGHT - 15)

    screen.blit(text, textRect)

    # Set up game timer display
    timer = font.render(game_timer(), True, white)

    timerRect = timer.get_rect()

    # Set the position of the timer to the bottom right of the screen
    timerRect.bottomright = (SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10)

    screen.blit(timer, timerRect)

    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(60)

pygame.quit()
print(SCORE)
