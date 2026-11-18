import pygame
pygame.init()

background_image = pygame.image.load('background.png')
background_image = pygame.transform.scale(background_image, (800, 500))


class Player:
    def __init__(self, x, y, width, height, image):
        self.original_image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.gravity = 0.5
        self.base_gravity = 0.5
        self.jump_power = -10
        self.vel_y = 0
        self.can_jump = False
        self.jumps = 2
        # === НОВЫЕ ПОЛЯ ДЛЯ ЧИТОВ ===
        self.money = 0
        self.god_mode = False
        self.infinite_fly = False
        self.speed_multiplier = 1.0
        self.jump_power_multiplier = 1.0

    def move(self):
        if not self.infinite_fly:
            self.vel_y += self.gravity
        self.rect.y += self.vel_y

        for w in walls:
            if self.rect.colliderect(w.rect):
                self.jumps = 2
                if self.vel_y > 0:
                    self.rect.bottom = w.rect.top
                    self.vel_y = 0
                    self.can_jump = True
                elif self.vel_y < 0:
                    self.rect.top = w.rect.bottom
                    self.vel_y = 0

    def jump(self):
        if self.can_jump:
            self.vel_y = self.jump_power * self.jump_power_multiplier
            if self.jumps <= 1:
                self.can_jump = False
            self.jumps -= 1

    def move_horizontal(self, dx):
        self.jumps = 2
        dx *= self.speed_multiplier
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                    self.vel_y = 0.1
                elif dx < 0:
                    self.rect.left = wall.rect.right
                    self.vel_y = 0.1


class Wall:
    def __init__(self, x, y, width, height, color=(22, 26, 31)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)


window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Val Kickers")

player = Player(100, 100, 50, 50, 'player.png')

walls = [
    Wall(20, 100, 200, 1000),
    Wall(350, 100, 150, 400),
    Wall(100, 450, 500, 400),
]

white = (255, 255, 255)

clock = pygame.time.Clock()

# === СОСТОЯНИЕ СЕКРЕТНОГО МЕНЮ ===
game_state = "play"   # "play" или "secret_menu"
menu_selection = 0
menu_options = [
    "Деньги +1000",
    "Бессмертие",
    "Бесконечный полёт",
    "Супер-скорость",
    "Супер-прыжок",
    "Закрыть меню",
]

game = True
move_left = False
move_right = False

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        if game_state == "play":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    move_right = True
                if event.key == pygame.K_a:
                    move_left = True
                if event.key == pygame.K_w and not player.infinite_fly:
                    player.jump()
                if event.key == pygame.K_F1:
                    game_state = "secret_menu"
                    menu_selection = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    move_right = False
                if event.key == pygame.K_a:
                    move_left = False

        elif game_state == "secret_menu":
            # Ловим KEYUP движения, чтобы клавиши не "залипали" после меню
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    move_right = False
                if event.key == pygame.K_a:
                    move_left = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu_selection = (menu_selection - 1) % len(menu_options)
                if event.key == pygame.K_DOWN:
                    menu_selection = (menu_selection + 1) % len(menu_options)
                if event.key == pygame.K_ESCAPE:
                    game_state = "play"
                if event.key == pygame.K_RETURN:
                    if menu_selection == 0:
                        player.money += 1000
                    elif menu_selection == 1:
                        player.god_mode = not player.god_mode
                    elif menu_selection == 2:
                        player.infinite_fly = not player.infinite_fly
                        if player.infinite_fly:
                            player.gravity = 0
                            player.vel_y = 0
                        else:
                            player.gravity = player.base_gravity
                    elif menu_selection == 3:
                        player.speed_multiplier = 2.0 if player.speed_multiplier == 1.0 else 1.0
                    elif menu_selection == 4:
                        player.jump_power_multiplier = 1.5 if player.jump_power_multiplier == 1.0 else 1.0
                    elif menu_selection == 5:
                        game_state = "play"

    # === ЛОГИКА ПОЛЁТА (если включён бесконечный полёт) ===
    if game_state == "play" and player.infinite_fly:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.vel_y = -5
        elif keys[pygame.K_s]:
            player.vel_y = 5
        else:
            player.vel_y = 0

    # === ОТРИСОВКА ===
    window.blit(background_image, (0, 0))

    if game_state == "play":
        player.move()
        if move_right:
            player.move_horizontal(3)
        if move_left:
            player.move_horizontal(-3)

        for wall in walls:
            wall.draw(window)
        window.blit(player.image, (player.rect.x, player.rect.y))

    elif game_state == "secret_menu":
        # Фон + игра
        for wall in walls:
            wall.draw(window)
        window.blit(player.image, (player.rect.x, player.rect.y))

        # Затемнение
        s = pygame.Surface((500, 500))
        s.set_alpha(180)
        s.fill((0, 0, 0))
        window.blit(s, (0, 0))

        font = pygame.font.Font(None, 36)
        title = font.render("СЕКРЕТНОЕ МЕНЮ", True, (255, 255, 0))
        window.blit(title, (130, 25))

        font_small = pygame.font.Font(None, 28)
        for i, opt in enumerate(menu_options):
            color = (0, 255, 0) if i == menu_selection else (255, 255, 255)
            text = font_small.render(opt, True, color)
            window.blit(text, (60, 80 + i * 35))

        status_font = pygame.font.Font(None, 22)
        y = 320
        window.blit(status_font.render(f"Деньги: {player.money}", True, (255, 255, 255)), (20, y))
        window.blit(status_font.render(f"Бессмертие: {'ВКЛ' if player.god_mode else 'ВЫКЛ'}", True, (255, 255, 255)), (20, y + 20))
        window.blit(status_font.render(f"Полёт: {'ВКЛ' if player.infinite_fly else 'ВЫКЛ'}", True, (255, 255, 255)), (20, y + 40))
        window.blit(status_font.render(f"Скорость: x{player.speed_multiplier}", True, (255, 255, 255)), (20, y + 60))
        window.blit(status_font.render(f"Прыжок: x{player.jump_power_multiplier}", True, (255, 255, 255)), (20, y + 80))
        window.blit(status_font.render("Enter - выбрать, ESC - выход", True, (180, 180, 180)), (120, 470))

    clock.tick(60)
    pygame.display.update()

pygame.quit()
