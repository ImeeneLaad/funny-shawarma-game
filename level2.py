import pygame
import sys
import random

WIDTH, HEIGHT = 1100, 700
FPS = 60

PLATFORMS = [
    pygame.Rect(80, 410, 130, 20), #x , y , largeur , hauteur
    pygame.Rect(270, 370, 100, 20),
    pygame.Rect(450, 280, 170, 20),
    pygame.Rect(730, 375, 320, 20),
]

class Dodger:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("Pictures/imene.png").convert_alpha(), (120, 160))
        self.rect = self.image.get_rect(midbottom=(60, HEIGHT - 50))
        self.vel_y = 0
        self.jump_strength = 23
        self.gravity = 1
        self.on_ground = False
        self.glitch_timer = 0

    def update(self, keys):
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += 5

        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        if self.rect.bottom >= HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        for plat in PLATFORMS:
            if self.rect.colliderect(plat) and self.vel_y > 0:
                if self.rect.bottom - self.vel_y <= plat.top:
                    self.rect.bottom = plat.top
                    self.vel_y = 0
                    self.on_ground = True

        if self.on_ground and (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]):
            self.vel_y = -self.jump_strength
            self.on_ground = False

        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        if self.glitch_timer > 0:
            self.glitch_timer -= 1

    def draw(self, screen):
        if self.glitch_timer == 0 or self.glitch_timer % 10 < 5:
            screen.blit(self.image, self.rect)

    def trigger_glitch(self):
        self.glitch_timer = 60

class FoodCoin:
    def __init__(self, image_path, pos, food_type):
        self.original_image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (40, 40))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=pos)
        self.food_type = food_type
        self.angle = 0
        self.collected = False

    def update(self):
        if not self.collected:
            self.angle = (self.angle + 3) % 360
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, self.rect)

    def check_collision(self, player_rect):
        if not self.collected and self.rect.colliderect(player_rect):
            self.collected = True
            return self.food_type
        return None

class EnemyNour:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("Pictures/Nour.png").convert_alpha(), (100, 140))
        self.rect = self.image.get_rect(midbottom=(900, HEIGHT - 50))
        self.speed = 3
        self.direction = random.choice([-1, 1])
        self.jump_vel = 0
        self.gravity = 1
        self.is_jumping = False
        self.flipflop_img = pygame.transform.scale(pygame.image.load("Pictures/knife.png").convert_alpha(), (40, 40))
        self.projectiles = []

    def update(self):
        self.rect.x += self.direction * self.speed

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1

        if random.random() < 0.01:
            self.direction *= -1

        if not self.is_jumping and random.random() < 0.01:
            self.is_jumping = True
            self.jump_vel = -15

        if self.is_jumping:
            self.rect.y += self.jump_vel
            self.jump_vel += self.gravity
            if self.rect.bottom >= HEIGHT - 50:
                self.rect.bottom = HEIGHT - 50
                self.is_jumping = False
                self.jump_vel = 0

        if random.random() < 0.02:
            flip_rect = self.flipflop_img.get_rect(midleft=(self.rect.left, self.rect.centery))
            self.projectiles.append(flip_rect)

        for f in self.projectiles[:]:
            f.x -= 10
            if f.right < 0:
                self.projectiles.remove(f)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for f in self.projectiles:
            screen.blit(self.flipflop_img, f)

def draw_hearts(screen, lives, heart_img, heart_black_img):
    for i in range(3):
        x = 10 + i * 50  
        y = 10           
        if i < lives:
            screen.blit(heart_img, (x, y))
        else:
            screen.blit(heart_black_img, (x, y))

class Level2:
    def __init__(self, screen, lives, collected_counts):
        self.screen = screen
        self.lives = lives
        self.collected_counts = collected_counts

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        background = pygame.transform.scale(pygame.image.load("Pictures/bg2.jpg").convert(), (WIDTH, HEIGHT))
        dodger = Dodger()
        enemy_nour = EnemyNour()

        food_items = [
            FoodCoin("Pictures/Pizza.png", (300, 600), "pizza"),
            FoodCoin("Pictures/Pizza.png", (500, 400), "pizza"),
            FoodCoin("Pictures/Burger.png", (600, 550), "burger"),
            FoodCoin("Pictures/Burger.png", (800, 420), "burger"),
            FoodCoin("Pictures/Frites.png", (900, 500), "fries"),
            FoodCoin("Pictures/Frites.png", (700, 350), "fries"),
            FoodCoin("Pictures/Pizza.png", (80, 410), "pizza"),
            FoodCoin("Pictures/Pizza.png", (80, 450), "pizza"),
            FoodCoin("Pictures/Burger.png", (270, 370), "burger"),
            FoodCoin("Pictures/Burger.png", (270, 370), "burger"),
            FoodCoin("Pictures/Frites.png", (730, 370), "fries"),
            FoodCoin("Pictures/Frites.png", (730, 375), "fries")
        ]

        required_counts = {"pizza": 2, "burger": 2, "fries": 1}
        pizza_icon = pygame.transform.scale(pygame.image.load("Pictures/Pizza.png").convert_alpha(), (30, 30))
        burger_icon = pygame.transform.scale(pygame.image.load("Pictures/Burger.png").convert_alpha(), (30, 30))
        fries_icon = pygame.transform.scale(pygame.image.load("Pictures/Frites.png").convert_alpha(), (30, 30))

        font = pygame.font.SysFont(None, 30)
        heart_font = pygame.font.SysFont("comicsansms", 72, bold=True)

        damage_cooldown = 0
        heart_img = pygame.transform.scale(pygame.image.load("Pictures/heart.png").convert_alpha(), (30, 30))
        heart_black_img = pygame.transform.scale(pygame.image.load("Pictures/heart_black.png").convert_alpha(), (30, 30))
        game_over = False
        win = False

        running = True
        while running:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if not game_over and not win:
                dodger.update(keys)
                enemy_nour.update()

                if damage_cooldown == 0:
                    if dodger.rect.colliderect(enemy_nour.rect):
                        self.lives -= 1
                        damage_cooldown = 60
                        dodger.trigger_glitch()
                    else:
                        for f in enemy_nour.projectiles:
                            if dodger.rect.colliderect(f):
                                self.lives -= 1
                                damage_cooldown = 60
                                dodger.trigger_glitch()
                                enemy_nour.projectiles.remove(f)
                                break
                else:
                    damage_cooldown -= 1

                if dodger.rect.right >= WIDTH:
                    if all(self.collected_counts[k] >= required_counts[k] for k in required_counts):
                        win = True

                if self.lives <= 0:
                    game_over = True

                for food in food_items:
                    food.update()
                    collected = food.check_collision(dodger.rect)
                    if collected:
                        self.collected_counts[collected] += 1

            self.screen.blit(background, (0, 0))
            dodger.draw(self.screen)
            enemy_nour.draw(self.screen)

            for food in food_items:
                food.draw(self.screen)

            x_base = WIDTH - 300
            self.screen.blit(pizza_icon, (x_base, 10))
            self.screen.blit(font.render(f"x {self.collected_counts['pizza']}", True, (255, 255, 255)), (x_base + 40, 15))

            self.screen.blit(burger_icon, (x_base + 100, 10))
            self.screen.blit(font.render(f"x {self.collected_counts['burger']}", True, (255, 255, 255)), (x_base + 140, 15))

            self.screen.blit(fries_icon, (x_base + 200, 10))
            self.screen.blit(font.render(f"x {self.collected_counts['fries']}", True, (255, 255, 255)), (x_base + 240, 15))

            draw_hearts(self.screen, self.lives, heart_img, heart_black_img)

            if game_over:
                text = heart_font.render("GAME OVER", True, (255, 0, 0))
                self.screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))
            elif win:
                text = heart_font.render("YOU WIN!", True, (0, 255, 0))
                self.screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))
                text2 = font.render("Press ENTER to continue to Level 3", True, (255, 255, 255))
                self.screen.blit(text2, text2.get_rect(center=(WIDTH//2, HEIGHT//2 + 60)))

                if keys[pygame.K_RETURN]:
                    from Level3 import Level3
                    level3_instance = Level3(self.screen, self.lives, self.collected_counts)
                    self.lives, self.collected_counts = level3_instance.run()
                    return self.lives, self.collected_counts



            pygame.display.flip()
            clock.tick(FPS)

        return self.lives, self.collected_counts
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Level 2 Test")

    initial_lives = 3
    initial_collected_counts = {"pizza": 0, "burger": 0, "fries": 0}

    level2 = Level2(screen, initial_lives, initial_collected_counts)
    lives, collected_counts = level2.run()


    pygame.quit()
