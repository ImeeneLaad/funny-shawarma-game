import pygame
import sys

def start_screen(screen):
    clock = pygame.time.Clock()

    # Load and scale images
    shawarma_img = pygame.image.load("Pictures/shawarma.png").convert_alpha()
    shawarma_original = pygame.transform.smoothscale(shawarma_img, (100, 100))

    pizza_img = pygame.image.load("Pictures/Pizza.png").convert_alpha()
    pizza_original = pygame.transform.smoothscale(pizza_img, (40, 40))

    frites_img = pygame.image.load("Pictures/Frites.png").convert_alpha()
    frites_original = pygame.transform.smoothscale(frites_img, (40, 40))

    burger_img = pygame.image.load("Pictures/Burger.png").convert_alpha()
    burger_original = pygame.transform.smoothscale(burger_img, (40, 40))

    # Fonts
    font_title = pygame.font.Font("PressStart2P-Regular.ttf", 40)
    font_text = pygame.font.Font("PressStart2P-Regular.ttf", 15)
    font_button = pygame.font.Font("PressStart2P-Regular.ttf", 24)

    # Angles for rotation
    shawarma_angle = 0
    food_angle = 0

    # Start button
    button_width, button_height = 200, 60
    button_x = (screen.get_width() - button_width) // 2
    button_y = screen.get_height() - button_height - 40
    start_button = pygame.Rect(button_x, button_y, button_width, button_height)

    while True:
        screen.fill((25, 25, 40))  # Background color

        # Title
        title = font_title.render("THE SHAWARMA QUEST", True, (255, 215, 0))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 60))
        screen.blit(title, title_rect)

        # Intro text
        intro_lines = [
            "After exams, Imene craved only one thing: shawarma.",
            "But her own friends betrayed her and stole it. Revenge begins now !!!"
        ]
        for i, line in enumerate(intro_lines):
            text = font_text.render(line, True, (200, 200, 200))
            text_rect = text.get_rect(center=(screen.get_width() // 2, 120 + i * 25))
            screen.blit(text, text_rect)

        # Character labels only
        labels = [
            ("Rieb: throws cats", (255, 100, 100), 180),
            ("Nour: throws knives", (100, 200, 255), 210),
            ("Kamel: guards shawarma", (255, 150, 50), 240)
        ]
        for label_text, color, y in labels:
            label = font_text.render(label_text, True, color)
            label_rect = label.get_rect(center=(screen.get_width() // 2, y))
            screen.blit(label, label_rect)

        # Spinning shawarma
        shawarma_angle = (shawarma_angle + 2) % 360
        rotated_shawarma = pygame.transform.rotate(shawarma_original, shawarma_angle)
        shawarma_rect = rotated_shawarma.get_rect(center=(screen.get_width() // 2, 320))
        screen.blit(rotated_shawarma, shawarma_rect)

        # Tip below shawarma
        tip_text = font_text.render("Remember: Grab 18+ FoodCoins or say goodbye to your shawarma feast!", True, (255, 255, 150))
        tip_rect = tip_text.get_rect(center=(screen.get_width() // 2, 370))
        screen.blit(tip_text, tip_rect)

        # Spinning FoodCoins (Pizza, Frites, Burger)
        food_angle = (food_angle + 3) % 360
        pizza = pygame.transform.rotate(pizza_original, food_angle)
        frites = pygame.transform.rotate(frites_original, food_angle)
        burger = pygame.transform.rotate(burger_original, food_angle)

        screen.blit(pizza, (screen.get_width() // 2 - 90, 410))
        screen.blit(frites, (screen.get_width() // 2 - 20, 410))
        screen.blit(burger, (screen.get_width() // 2 + 50, 410))

        # Start button
        pygame.draw.rect(screen, (0, 200, 100), start_button, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), start_button, 2, border_radius=12)
        button_text = font_button.render("START", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=start_button.center)
        screen.blit(button_text, button_text_rect)

        pygame.display.flip()
        clock.tick(60)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return
