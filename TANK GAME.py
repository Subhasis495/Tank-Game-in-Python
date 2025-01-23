import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)

# Tank settings
TANK_WIDTH, TANK_HEIGHT = 60, 30
TANK_BARREL_WIDTH, TANK_BARREL_HEIGHT = 7, 50
BULLET_RADIUS = 5
BULLET_SPEED = 7
BARREL_ROTATION_SPEED = 3
GRAVITY = 0.1  
MAX_HEALTH = 100

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Game")

# Load background image
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Load sounds
game_over_sound = pygame.mixer.Sound("game over.mp3")
tank_movement_sound = pygame.mixer.Sound("tank movement 3.mp3")
firing_sound = pygame.mixer.Sound("firing.mp3")
pygame.mixer.Sound.set_volume(tank_movement_sound, 0.2)  

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Explosion settings
EXPLOSION_DURATION = 20  

# Tank class
class Tank:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.speed = 5
        self.bullets = []
        self.barrel_angle = 45  
        self.shoot_delay = 300 
        self.last_shot_time = pygame.time.get_ticks()
        self.health = MAX_HEALTH
        self.is_moving = False

    def draw(self):
        # Draw tank body
        pygame.draw.rect(screen, self.color, (self.x, self.y, TANK_WIDTH, TANK_HEIGHT))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, TANK_WIDTH, TANK_HEIGHT), 2)

        # Draw tank barrel
        barrel_x = self.x + TANK_WIDTH // 2
        barrel_y = self.y + TANK_HEIGHT // 2
        barrel_end_x = barrel_x + TANK_BARREL_HEIGHT * math.cos(math.radians(self.barrel_angle))
        barrel_end_y = barrel_y - TANK_BARREL_HEIGHT * math.sin(math.radians(self.barrel_angle))
        pygame.draw.line(screen, BLACK, (barrel_x, barrel_y), (barrel_end_x, barrel_end_y), TANK_BARREL_WIDTH)
        pygame.draw.rect(screen, BLACK, (barrel_end_x - 5, barrel_end_y - 5, 10, 10))

        # Draw bullets
        for bullet in self.bullets:
            pygame.draw.circle(screen, self.color, (int(bullet[0]), int(bullet[1])), BULLET_RADIUS)
            pygame.draw.circle(screen, BLACK, (int(bullet[0]), int(bullet[1])), BULLET_RADIUS, 1)

        # Draw health bar
        health_bar_width = 50
        health_bar_height = 7
        health_ratio = self.health / MAX_HEALTH
        health_color = GREEN if health_ratio > 0.5 else (255, 255 * health_ratio * 2, 0)
        pygame.draw.rect(screen, health_color, (self.x, self.y - 10, int(health_bar_width * health_ratio), health_bar_height))
        pygame.draw.rect(screen, BLACK, (self.x, self.y - 10, health_bar_width, health_bar_height), 1)

    def move(self, keys, forward, backward, obstacles):
        self.is_moving = False
        if keys[forward]:
            new_x = self.x - self.speed
            if new_x > 0 and not self.check_collision_with_obstacles(new_x, self.y, obstacles):
                self.x = new_x
                self.is_moving = True
        if keys[backward]:
            new_x = self.x + self.speed
            if new_x < WIDTH - TANK_WIDTH and not self.check_collision_with_obstacles(new_x, self.y, obstacles):
                self.x = new_x
                self.is_moving = True

        if self.is_moving:
            if not pygame.mixer.get_busy():
                tank_movement_sound.play()

    def check_collision_with_obstacles(self, x, y, obstacles):
        tank_rect = pygame.Rect(x, y, TANK_WIDTH, TANK_HEIGHT)
        for obstacle in obstacles:
            if tank_rect.colliderect(obstacle):
                return True
        return False

    def rotate_barrel(self, keys, rotate_left, rotate_right):
        if keys[rotate_left]:
            self.barrel_angle = (self.barrel_angle + BARREL_ROTATION_SPEED) % 180
        if keys[rotate_right]:
            self.barrel_angle = (self.barrel_angle - BARREL_ROTATION_SPEED) % 180

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_delay:
            barrel_x = self.x + TANK_WIDTH // 2 + TANK_BARREL_HEIGHT * math.cos(math.radians(self.barrel_angle))
            barrel_y = self.y + TANK_HEIGHT // 2 - TANK_BARREL_HEIGHT * math.sin(math.radians(self.barrel_angle))
            self.bullets.append([barrel_x, barrel_y, self.barrel_angle, 0]) 
            self.last_shot_time = current_time
            firing_sound.play()  

    def update_bullets(self, obstacles):
        for bullet in self.bullets:
            bullet[0] += BULLET_SPEED * math.cos(math.radians(bullet[2]))
            bullet[1] -= BULLET_SPEED * math.sin(math.radians(bullet[2])) - bullet[3]
            bullet[3] += GRAVITY  
            for obstacle in obstacles:
                if obstacle.collidepoint(bullet[0], bullet[1]):
                    self.bullets.remove(bullet)
                    break
        self.bullets = [bullet for bullet in self.bullets if 0 < bullet[0] < WIDTH and 0 < bullet[1] < HEIGHT]

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

# Explosion class
class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0

    def draw(self):
        if self.frame < EXPLOSION_DURATION:
            radius = self.frame * 3  
            pygame.draw.circle(screen, ORANGE, (self.x, self.y), radius)
            pygame.draw.circle(screen, YELLOW, (self.x, self.y), radius // 2)
            self.frame += 1

# Collision detection
def check_collision(tank, bullets, explosions):
    for bullet in bullets:
        if tank.x < bullet[0] < tank.x + TANK_WIDTH and tank.y < bullet[1] < tank.y + TANK_HEIGHT:
            explosions.append(Explosion(int(bullet[0]), int(bullet[1])))  
            bullets.remove(bullet)
            tank.take_damage(20)  
            return True
    return False

# Main game function
def main():
    run = True
    ground_level = HEIGHT - 145  
    tank1 = Tank(100, ground_level, RED)
    tank2 = Tank(WIDTH - 140, ground_level, BLUE)

    # Obstacles
    obstacles = [
        pygame.Rect(300, ground_level - 120, 50, 150),
        pygame.Rect(400, ground_level - 100, 50, 130),
        pygame.Rect(500, ground_level - 110, 50, 140),
    ]

    explosions = []  
    game_over_message = ""

    while run:
        clock.tick(40)

        # Draw background
        screen.blit(background_image, (0, 0))

        # Draw obstacles
        for obstacle in obstacles:
            pygame.draw.rect(screen, BROWN, obstacle)
            pygame.draw.rect(screen, BLACK, obstacle, 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Tank movement
        keys = pygame.key.get_pressed()
        tank1.move(keys, pygame.K_a, pygame.K_d, obstacles)
        tank2.move(keys, pygame.K_LEFT, pygame.K_RIGHT, obstacles)

        # Barrel rotation
        tank1.rotate_barrel(keys, pygame.K_w, pygame.K_s)
        tank2.rotate_barrel(keys, pygame.K_DOWN, pygame.K_UP)

        
        if keys[pygame.K_SPACE]:
            tank1.shoot()
        if keys[pygame.K_RETURN]:
            tank2.shoot()

        # Update bullets
        tank1.update_bullets(obstacles)
        tank2.update_bullets(obstacles)

        # Check collisions
        check_collision(tank1, tank2.bullets, explosions)
        check_collision(tank2, tank1.bullets, explosions)

        # Draw tanks and bullets
        tank1.draw()
        tank2.draw()

        # Draw explosions
        for explosion in explosions:
            explosion.draw()
        explosions = [explosion for explosion in explosions if explosion.frame < EXPLOSION_DURATION]

        
        if tank1.health <= 0:
            game_over_message = "Tank 1 destroyed!"
            run = False
        if tank2.health <= 0:
            game_over_message = "Tank 2 destroyed!"
            run = False

        
        pygame.display.flip()

    # Play game over sound
    game_over_sound.play()

    
    font = pygame.font.SysFont(None, 55)
    text = font.render(game_over_message, True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

if __name__ == "__main__":
    main()
