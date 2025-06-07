import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1100, 700
FPS = 60

class Dodger:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("Pictures/imene.png").convert_alpha(), (120, 160))
        self.rect = self.image.get_rect(midbottom=(60, HEIGHT - 50))
        self.is_jumping = False
        self.jump_vel = 0
        self.jump_strength = 20
        self.gravity = 1
        self.speed = 7
        self.glitch_timer = 0

    def update(self, keys):
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
            if self.rect.bottom >= HEIGHT - 50:
                self.rect.bottom = HEIGHT - 50
                self.is_jumping = False
                self.jump_vel = 0

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

class Enemy:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("Pictures/Rieb.png").convert_alpha(), (120, 160))
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 50))
        self.direction = random.choice([-1, 1])
        self.speed = 3
        self.cat_image = pygame.transform.scale(pygame.image.load("Pictures/cat.png").convert_alpha(), (40, 40))
        self.cat_speed = 10
        self.cats = []

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1
        if random.random() < 0.01:
            self.direction *= -1
        if random.random() < 0.02:
            self.throw_cat()

        for cat in self.cats[:]:
            cat.x -= self.cat_speed
            if cat.right < 0:
                self.cats.remove(cat)

    def throw_cat(self):
        hand_pos = (self.rect.left + 50, self.rect.top + 100)
        cat_rect = self.cat_image.get_rect(center=hand_pos)
        self.cats.append(cat_rect)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for cat in self.cats:
            screen.blit(self.cat_image, cat)

    def get_hitbox(self):
        return self.rect.inflate(-20, -20)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Rieb Level")
        self.clock = pygame.time.Clock()
        self.background = pygame.transform.scale(pygame.image.load("Pictures/bg1.jpg").convert(), (WIDTH, HEIGHT))
        self.dodger = Dodger()
        self.enemy = Enemy()
        self.lives = 3
        self.game_over = False
        self.win = False
        self.damage_cooldown = 0
        self.heart_image = pygame.transform.scale(pygame.image.load("Pictures/heart.png").convert_alpha(), (40, 40))
        self.heart_black_image = pygame.transform.scale(pygame.image.load("Pictures/heart_black.png").convert_alpha(), (40, 40))

    def reset(self):
        self.__init__()

    def draw_hearts(self):
        for i in range(3):
            heart_x = 10 + i * 50
            if i < self.lives:
                self.screen.blit(self.heart_image, (heart_x, 10))
            else:
                self.screen.blit(self.heart_black_image, (heart_x, 10))

    def draw_message_box(self, title_text, sub_text, title_color, sub_color):
        box_width, box_height = 600, 300
        box_rect = pygame.Rect((WIDTH - box_width) // 2, (HEIGHT - box_height) // 2, box_width, box_height)
        pygame.draw.rect(self.screen, (30, 30, 30), box_rect, border_radius=20)
        pygame.draw.rect(self.screen, (255, 255, 255), box_rect, width=4, border_radius=20)

        title_font = pygame.font.SysFont("comicsansms", 72, bold=True)
        title_surface = title_font.render(title_text, True, title_color)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
        self.screen.blit(title_surface, title_rect)

        sub_font = pygame.font.SysFont("comicsansms", 36)
        sub_surface = sub_font.render(sub_text, True, sub_color)
        sub_rect = sub_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        self.screen.blit(sub_surface, sub_rect)

    def check_collisions(self):
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        dodger_hitbox = self.dodger.get_hitbox()
        enemy_hitbox = self.enemy.get_hitbox()

        for cat in self.enemy.cats[:]:
            if dodger_hitbox.colliderect(cat) and self.damage_cooldown == 0:
                self.lives -= 1
                self.damage_cooldown = 60
                self.dodger.trigger_glitch()
                self.enemy.cats.remove(cat)

        if dodger_hitbox.colliderect(enemy_hitbox) and self.damage_cooldown == 0:
            self.lives -= 1
            self.damage_cooldown = 60
            self.dodger.trigger_glitch()

        if self.lives <= 0:
            self.game_over = True

    def run(self):
        running = True
        while running:
            keys = pygame.key.get_pressed()
            enter_pressed = False
            restart_pressed = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        enter_pressed = True
                    if event.key == pygame.K_r:
                        restart_pressed = True

            self.screen.blit(self.background, (0, 0))

            if not self.game_over and not self.win:
                self.dodger.update(keys)
                self.enemy.update()
                self.check_collisions()
                if self.dodger.rect.right >= WIDTH:
                    self.win = True

            self.enemy.draw(self.screen)
            self.dodger.draw(self.screen)
            self.draw_hearts()

            if self.game_over:
                self.draw_message_box("GAME OVER", "Press R to Restart", (255, 0, 0), (255, 255, 255))
            elif self.win:
                self.draw_message_box("YOU WIN!", "Press ENTER for Level 2", (0, 255, 0), (255, 255, 255))
                if enter_pressed:
                    from level2 import Level2
                    collected_counts = {"pizza": 0, "burger": 0, "fries": 0}  
                    level2_instance = Level2(self.screen, self.lives, collected_counts)
                    self.lives, collected_counts = level2_instance.run()
                    self.win = False
                    self.game_over = False
                    self.reset()

            if self.game_over and restart_pressed:
                self.reset()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
