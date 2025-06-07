import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 1100, 700
FPS = 60

class Player:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("Pictures/imene.png").convert_alpha(), (80, 140))
        self.rect = self.image.get_rect(midbottom=(60, HEIGHT - 140))
        self.is_jumping = False
        self.jump_vel = 0
        self.jump_strength = 20
        self.gravity = 1
        self.speed = 7
        self.glitch_timer = 0

    def update(self, keys, platforms):
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if not self.is_jumping and keys[pygame.K_SPACE]:
            self.is_jumping = True
            self.jump_vel = -self.jump_strength

        if self.is_jumping:
            self.rect.y += self.jump_vel
            self.jump_vel += self.gravity

        on_platform = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.jump_vel >= 0:
                if self.rect.bottom <= platform.rect.top + 15:
                    self.rect.bottom = platform.rect.top
                    self.is_jumping = False
                    self.jump_vel = 0
                    on_platform = True
                    break

        if self.rect.bottom >= HEIGHT - 140:
            self.rect.bottom = HEIGHT - 140
            self.is_jumping = False
            self.jump_vel = 0
        elif not on_platform:
            self.is_jumping = True

        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))
        if self.glitch_timer > 0:
            self.glitch_timer -= 1

    def draw(self, screen):
        if self.glitch_timer == 0 or self.glitch_timer % 10 < 5:
            screen.blit(self.image, self.rect)

    def trigger_glitch(self):
        self.glitch_timer = 60

    def get_hitbox(self):
        return self.rect.inflate(-20, -20)

class Boss:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("Pictures/Kamel.png").convert_alpha(), (120, 180))
        self.rect = self.image.get_rect(midbottom=(WIDTH - 100, HEIGHT - 50))
        self.direction = random.choice([-1, 1])
        self.speed = 3
        self.jump_vel = 2
        self.is_jumping = False
        self.jump_strength = 4
        self.gravity = 1
        self.projectile_image = pygame.transform.scale(pygame.image.load("Pictures/fire.png").convert_alpha(), (50, 50))
        self.projectiles = []
        self.projectile_speed = 8

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left <= WIDTH // 2 or self.rect.right >= WIDTH:
            self.direction *= -1
        if random.random() < 0.02:
            self.direction *= -1

        if not self.is_jumping and random.random() < 0.01:
            self.is_jumping = True
            self.jump_vel = -self.jump_strength

        if self.is_jumping:
            self.rect.y += self.jump_vel
            self.jump_vel += self.gravity
        if self.rect.bottom >= HEIGHT - 140:
            self.rect.bottom = HEIGHT - 140
            self.is_jumping = False
            self.jump_vel = 0

        if random.random() < 0.001:
            self.shoot()

        for p in self.projectiles[:]:
            p.x -= self.projectile_speed
            if p.right < 0:
                self.projectiles.remove(p)

    def shoot(self):
        hand_pos = (self.rect.left + 40, self.rect.top + 90)
        proj_rect = self.projectile_image.get_rect(center=hand_pos)
        self.projectiles.append(proj_rect)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for p in self.projectiles:
            screen.blit(self.projectile_image, p)

    def get_hitbox(self):
        return self.rect.inflate(-20, -20)

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (100, 200, 100)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class FoodCoin:
    def __init__(self, image_path, pos, type_):
        self.original_image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (40, 40))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=pos)
        self.angle = 0
        self.type = type_
        self.collected = False

    def update(self):
        self.angle = (self.angle + 3) % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, self.rect)

initial_counts = {"pizza": 0, "burger": 0, "fries": 0}

class Level3:
    def __init__(self, screen, lives, collected_counts):
        self.screen = screen
        pygame.display.set_caption("Level 3: Final Battle")
        self.clock = pygame.time.Clock()
        self.background = pygame.transform.scale(pygame.image.load("Pictures/bg3.jpg").convert(), (WIDTH, HEIGHT))
        self.player = Player()
        self.boss = Boss()
        self.lives = lives
        self.collected_counts = collected_counts
        self.game_over = False
        self.win = False
        self.damage_cooldown = 0
        self.heart_img = pygame.transform.scale(pygame.image.load("Pictures/heart.png").convert_alpha(), (40, 40))
        self.heart_black_img = pygame.transform.scale(pygame.image.load("Pictures/heart_black.png").convert_alpha(), (40, 40))
        self.platforms = [
            Platform(50, 480, 200, 5),
            Platform(540, 387, 380, 5),
            Platform(510, 285, 120, 5),
            Platform(950, 285, 140, 5)
        ]
        self.shawarma_img = pygame.transform.scale(pygame.image.load("Pictures/shawarma.png").convert_alpha(), (80, 80))
        self.shawarma_angle = 0
        self.shawarma_pos = (750, 500)

        self.food_items = [
            FoodCoin("Pictures/Pizza.png", (150, 450), "pizza"),
            FoodCoin("Pictures/Pizza.png", (200, 450), "pizza"),
            FoodCoin("Pictures/Pizza.png", (250, 450), "pizza"),
            FoodCoin("Pictures/Burger.png", (580, 357), "burger"),
            FoodCoin("Pictures/Burger.png", (630, 357), "burger"),
            FoodCoin("Pictures/Burger.png", (680, 357), "burger"),
            FoodCoin("Pictures/Frites.png", (510, 255), "fries"),
            FoodCoin("Pictures/Frites.png", (560, 255), "fries"),
            FoodCoin("Pictures/Frites.png", (610, 255), "fries"),
        ]


        self.collected_counts = collected_counts.copy()
        self.required_counts = {"pizza": 3, "burger": 3, "fries": 3}

        self.pizza_icon = pygame.transform.scale(pygame.image.load("Pictures/Pizza.png").convert_alpha(), (30, 30))
        self.burger_icon = pygame.transform.scale(pygame.image.load("Pictures/Burger.png").convert_alpha(), (30, 30))
        self.fries_icon = pygame.transform.scale(pygame.image.load("Pictures/Frites.png").convert_alpha(), (30, 30))
        self.food_font = pygame.font.SysFont(None, 30)


    def draw_food_counter(self):
        x_start = WIDTH - 250  
        y = 10                 
        spacing = 80           

    # Pizza
        self.screen.blit(self.pizza_icon, (x_start, y))
        self.screen.blit(self.food_font.render(f"x {self.collected_counts['pizza']}", True, (255, 255, 255)), (x_start + 35, y + 5))

    # Burger
        self.screen.blit(self.burger_icon, (x_start + spacing, y))
        self.screen.blit(self.food_font.render(f"x {self.collected_counts['burger']}", True, (255, 255, 255)), (x_start + spacing + 35, y + 5))

    # Fries
        self.screen.blit(self.fries_icon, (x_start + 2 * spacing, y))
        self.screen.blit(self.food_font.render(f"x {self.collected_counts['fries']}", True, (255, 255, 255)), (x_start + 2 * spacing + 35, y + 5))


    def draw_shawarma(self):
        self.shawarma_angle = (self.shawarma_angle + 2) % 360
        rotated = pygame.transform.rotate(self.shawarma_img, self.shawarma_angle)
        rect = rotated.get_rect(center=self.shawarma_pos)
        self.screen.blit(rotated, rect)

    def draw_hearts(self):
        for i in range(3):
            x = 10 + i * 50
            if i < self.lives:
                self.screen.blit(self.heart_img, (x, 10))
            else:
                self.screen.blit(self.heart_black_img, (x, 10))

    def draw_message_box(self, title_text, sub_text, title_color, sub_color):
        box_rect = pygame.Rect((WIDTH - 600) // 2, (HEIGHT - 300) // 2, 600, 300)
        pygame.draw.rect(self.screen, (30, 30, 30), box_rect, border_radius=20)
        pygame.draw.rect(self.screen, (255, 255, 255), box_rect, width=4, border_radius=20)
        title_surface = pygame.font.SysFont("comicsansms", 72, bold=True).render(title_text, True, title_color)
        sub_surface = pygame.font.SysFont("comicsansms", 36).render(sub_text, True, sub_color)
        self.screen.blit(title_surface, title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60)))
        self.screen.blit(sub_surface, sub_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))

    def check_collisions(self):
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1
        hitbox = self.player.get_hitbox()
        if self.boss.get_hitbox().colliderect(hitbox) and self.damage_cooldown == 0:
            self.lives -= 1
            self.damage_cooldown = 60
            self.player.trigger_glitch()
        for p in self.boss.projectiles[:]:
            if hitbox.colliderect(p) and self.damage_cooldown == 0:
                self.lives -= 1
                self.damage_cooldown = 60
                self.player.trigger_glitch()
                self.boss.projectiles.remove(p)
        if self.lives <= 0:
            self.game_over = True

    def run(self):
        running = True
        while running:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.blit(self.background, (0, 0))
            #for platform in self.platforms:
                #platform.draw(self.screen)

            if not self.game_over and not self.win:
                self.player.update(keys, self.platforms)
                self.boss.update()
                self.check_collisions()
                for item in self.food_items:
                    item.update()
                    if not item.collected and self.player.rect.colliderect(item.rect):
                        item.collected = True
                        self.collected_counts[item.type] += 1
                total_food = sum(self.collected_counts.values())
                shawarma_rect = self.shawarma_img.get_rect(center=self.shawarma_pos)
                if self.player.rect.colliderect(shawarma_rect):
                    if total_food >= 18:
                        self.win = True
                    else:
                        self.draw_message_box("Collect More Food!", "You need at least 18 to win.", (255, 255, 0), (255, 255, 255))


            self.player.draw(self.screen)
            self.boss.draw(self.screen)
            for item in self.food_items:
                item.draw(self.screen)
            self.draw_shawarma()
            self.draw_hearts()
            self.draw_food_counter()

            if self.game_over:
                self.draw_message_box("GAME OVER", "Press ESC to Quit", (255, 0, 0), (255, 255, 255))
            elif self.win:
                self.draw_message_box("YOU WON!", "The Shawarma is Yours!", (0, 255, 0), (255, 255, 255))

            if self.game_over and keys[pygame.K_ESCAPE]:
                running = False

            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()

if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    initial_lives = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    initial_counts = {"pizza": 0, "burger": 0, "fries": 0}
    game = Level3(screen, initial_lives, initial_counts)
    game.run()

