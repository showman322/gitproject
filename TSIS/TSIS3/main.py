# =====================================================
# 1. IMPORTS
# =====================================================
import pygame
import sys
import random
import json
import os
import time
from pygame.locals import *


# =====================================================
# 2. PYGAME INIT — launch pygame
# =====================================================
pygame.init()
try:
    pygame.mixer.init()
except pygame.error:
    pass


# =====================================================
# 3. CONSTANTS — window sizes, road, colors, files
# =====================================================
FPS = 60
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
ROAD_LEFT = 40
ROAD_RIGHT = 360
LANES = [80, 160, 240, 320]
PLAYER_Y = 520
FINISH_DISTANCE = 3000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (40, 210, 70)
BLUE = (50, 150, 255)
YELLOW = (255, 220, 0)
ORANGE = (255, 140, 0)
GRAY = (120, 120, 120)
DARK_GRAY = (55, 55, 55)
PURPLE = (160, 80, 220)
CYAN = (0, 220, 255)
BROWN = (70, 40, 20)

ASSET_DIR = "racer"
SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"

DEFAULT_SETTINGS = {"sound": True, "car_color": "blue", "difficulty": "normal"}
CAR_COLORS = ["blue", "red", "green", "purple"]
DIFFICULTY = {
    "easy": {"speed": 4.0, "spawn_mult": 0.85},
    "normal": {"speed": 5.0, "spawn_mult": 1.0},
    "hard": {"speed": 6.0, "spawn_mult": 1.25},
}


# =====================================================
# 4. SCREEN AND FONTS — window, FPS, and fonts
# =====================================================
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("TSIS 3 Racer Game")
clock = pygame.time.Clock()

font_big = pygame.font.SysFont("Times New Roman", 52, bold=True)
font_mid = pygame.font.SysFont("Times New Roman", 30, bold=True)
font_small = pygame.font.SysFont("Times New Roman", 21)
font_tiny = pygame.font.SysFont("Times New Roman", 16)



# =====================================================
# 5. FILE HELPERS — paths, image loading, and JSON
# =====================================================
def asset_path(name):
    return os.path.join(ASSET_DIR, name)


def load_image(name, size=None):
    try:
        img = pygame.image.load(asset_path(name)).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except pygame.error:
        surf = pygame.Surface(size or (45, 75), pygame.SRCALPHA)
        pygame.draw.rect(surf, BLUE, surf.get_rect(), border_radius=8)
        pygame.draw.rect(surf, BLACK, surf.get_rect(), 2, border_radius=8)
        return surf


def load_json(path, default):
    if not os.path.exists(path):
        save_json(path, default)
        return default.copy() if isinstance(default, dict) else list(default)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception:
        save_json(path, default)
        return default.copy() if isinstance(default, dict) else list(default)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_settings():
    settings = load_json(SETTINGS_FILE, DEFAULT_SETTINGS)
    for k, v in DEFAULT_SETTINGS.items():
        settings.setdefault(k, v)
    if settings["car_color"] not in CAR_COLORS:
        settings["car_color"] = "blue"
    if settings["difficulty"] not in DIFFICULTY:
        settings["difficulty"] = "normal"
    return settings


def save_settings(settings):
    save_json(SETTINGS_FILE, settings)


def load_leaderboard():
    data = load_json(LEADERBOARD_FILE, [])
    return data if isinstance(data, list) else []


def save_score(name, score, distance, coins):
    board = load_leaderboard()
    board.append({
        "name": name or "Player",
        "score": int(score),
        "distance": int(distance),
        "coins": int(coins),
        "date": time.strftime("%Y-%m-%d %H:%M")
    })
    board.sort(key=lambda x: x.get("score", 0), reverse=True)
    save_json(LEADERBOARD_FILE, board[:10])



# =====================================================
# 6. UI HELPERS — buttons and text in the center
# =====================================================
class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        color = (225, 225, 225) if self.rect.collidepoint(pygame.mouse.get_pos()) else WHITE
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=8)
        img = font_small.render(self.text, True, BLACK)
        screen.blit(img, img.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def center_text(text, font, color, y):
    img = font.render(text, True, color)
    screen.blit(img, img.get_rect(center=(SCREEN_WIDTH // 2, y)))



# =====================================================
# 7. ASSETS — pictures, collision sound, music
# =====================================================
background_img = load_image("AnimatedStreet.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
player_base_img = load_image("Player.png", (44, 78))
enemy_img = load_image("Enemy.png", (44, 78))
crash_sound = None
try:
    crash_sound = pygame.mixer.Sound(asset_path("crash.wav"))
except Exception:
    crash_sound = None

background_music_loaded = False
try:
    pygame.mixer.music.load(asset_path("background.wav"))
    background_music_loaded = True
except Exception:
    background_music_loaded = False



# =====================================================
# 8. MUSIC AND ROAD — music and moving road
# =====================================================
def update_music(settings):
    if not background_music_loaded:
        return
    if settings.get("sound", True):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()


def draw_road(scroll=0):
    # Scrolling background: two copies of the road image move downward.
    # This makes it look like the player's car is driving forward.
    y = int(scroll) % SCREEN_HEIGHT
    screen.blit(background_img, (0, y))
    screen.blit(background_img, (0, y - SCREEN_HEIGHT))


def safe_lane(player_rect):
    # выбираем линию так, чтобы объект не появился прямо перед игроком
    safe = [x for x in LANES if not (player_rect.centery > 400 and abs(x - player_rect.centerx) < 70)]
    return random.choice(safe or LANES)



# =====================================================
# 9. GAME OBJECTS — player, enemies, coins, obstacles, bonuses
# =====================================================
class Player(pygame.sprite.Sprite):
    def __init__(self, color_name):
        super().__init__()
        self.image = player_base_img.copy()
        # optional color setting: blue keeps original image; other choices tint the blue car
        if color_name != "blue":
            tint = {"red": (255, 80, 80), "green": (70, 230, 90), "purple": (180, 100, 240)}[color_name]
            overlay = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            overlay.fill((*tint, 60))
            self.image.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        self.rect = self.image.get_rect(center=(LANES[1], PLAYER_Y))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > ROAD_LEFT:
            self.rect.move_ip(-6, 0)
        if keys[K_RIGHT] and self.rect.right < ROAD_RIGHT:
            self.rect.move_ip(6, 0)
        if keys[K_UP] and self.rect.top > 260:
            self.rect.move_ip(0, -4)
        if keys[K_DOWN] and self.rect.bottom < SCREEN_HEIGHT - 5:
            self.rect.move_ip(0, 4)


class TrafficCar(pygame.sprite.Sprite):
    def __init__(self, player_rect, extra_speed):
        super().__init__()
        self.image = enemy_img.copy()  # red car for enemies
        self.rect = self.image.get_rect(center=(safe_lane(player_rect), -90))
        self.extra_speed = extra_speed

    def move(self, speed):
        self.rect.move_ip(0, speed + self.extra_speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.value = random.choices([1, 2, 5], weights=[70, 25, 5])[0]
        size = 22 + self.value * 3
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (size // 2, size // 2), size // 2)
        pygame.draw.circle(self.image, WHITE, (size // 2, size // 2), size // 3, 2)
        label = font_tiny.render(str(self.value), True, BLACK)
        self.image.blit(label, label.get_rect(center=(size // 2, size // 2)))
        self.rect = self.image.get_rect(center=(random.choice(LANES), -30))

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super().__init__()
        self.kind = random.choice(["barrier", "oil", "pothole", "speed_bump", "moving_barrier"])
        self.image = pygame.Surface((58, 38), pygame.SRCALPHA)
        self.direction = random.choice([-2, 2]) if self.kind == "moving_barrier" else 0
        if self.kind in ["barrier", "moving_barrier"]:
            pygame.draw.rect(self.image, RED, (0, 8, 58, 22), border_radius=4)
            pygame.draw.line(self.image, WHITE, (8, 30), (22, 8), 4)
            pygame.draw.line(self.image, WHITE, (34, 30), (48, 8), 4)
        elif self.kind == "oil":
            pygame.draw.ellipse(self.image, BLACK, (3, 8, 52, 22))
            pygame.draw.ellipse(self.image, (45, 45, 45), (15, 12, 18, 8))
        elif self.kind == "pothole":
            pygame.draw.ellipse(self.image, BROWN, (2, 5, 54, 28))
            pygame.draw.ellipse(self.image, BLACK, (12, 10, 32, 15))
        else:
            pygame.draw.rect(self.image, ORANGE, (0, 12, 58, 12), border_radius=5)
            pygame.draw.rect(self.image, YELLOW, (0, 12, 58, 12), 2, border_radius=5)
        self.rect = self.image.get_rect(center=(safe_lane(player_rect), -45))

    def move(self, speed):
        self.rect.move_ip(self.direction, speed)
        if self.rect.left < ROAD_LEFT or self.rect.right > ROAD_RIGHT:
            self.direction *= -1
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.kind = random.choice(["nitro", "shield", "repair"])
        self.spawn_time = pygame.time.get_ticks()
        self.timeout = 6500
        self.image = pygame.Surface((36, 36), pygame.SRCALPHA)
        colors = {"nitro": CYAN, "shield": GREEN, "repair": RED}
        labels = {"nitro": "N", "shield": "S", "repair": "+"}
        pygame.draw.circle(self.image, colors[self.kind], (18, 18), 17)
        pygame.draw.circle(self.image, WHITE, (18, 18), 17, 2)
        txt = font_small.render(labels[self.kind], True, BLACK)
        self.image.blit(txt, txt.get_rect(center=(18, 18)))
        self.rect = self.image.get_rect(center=(random.choice(LANES), -40))

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT or pygame.time.get_ticks() - self.spawn_time > self.timeout:
            self.kill()


class NitroStrip(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super().__init__()
        self.image = pygame.Surface((62, 90), pygame.SRCALPHA)
        pygame.draw.rect(self.image, CYAN, (4, 0, 54, 90), border_radius=8)
        for y in range(8, 78, 22):
            pygame.draw.polygon(self.image, WHITE, [(31, y), (15, y + 18), (47, y + 18)])
        self.rect = self.image.get_rect(center=(safe_lane(player_rect), -95))

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()



# =====================================================
# 10. SCREENS — username, menu, settings, leaderboard, game over
# =====================================================
def username_screen():
    name = ""
    while True:
        screen.fill((25, 25, 25))
        center_text("Enter username", font_mid, WHITE, 170)
        box = pygame.Rect(65, 245, 270, 48)
        pygame.draw.rect(screen, WHITE, box, border_radius=8)
        pygame.draw.rect(screen, BLACK, box, 2, border_radius=8)
        screen.blit(font_small.render(name, True, BLACK), (box.x + 10, box.y + 12))
        center_text("Press ENTER to start", font_small, WHITE, 335)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    return name.strip() or "Player"
                if event.key == K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 12 and event.unicode.isprintable():
                    name += event.unicode
        pygame.display.update()
        clock.tick(FPS)


def main_menu(settings):
    buttons = [Button("Play", 120, 185, 160, 45), Button("Leaderboard", 120, 245, 160, 45),
               Button("Settings", 120, 305, 160, 45), Button("Quit", 120, 365, 160, 45)]
    while True:
        update_music(settings)
        screen.fill((35, 35, 35))
        center_text("RACER", font_big, YELLOW, 105)
        for b in buttons:
            b.draw()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            for i, b in enumerate(buttons):
                if b.clicked(event):
                    return ["play", "leaderboard", "settings", "quit"][i]
        pygame.display.update()
        clock.tick(FPS)


def settings_screen(settings):
    sound_btn = Button("Toggle sound", 95, 175, 210, 40)
    color_btn = Button("Change car color", 95, 270, 210, 40)
    diff_btn = Button("Change difficulty", 95, 365, 210, 40)
    back_btn = Button("Back", 120, 510, 160, 40)
    diffs = list(DIFFICULTY.keys())
    while True:
        update_music(settings)
        screen.fill((30, 30, 45))
        center_text("Settings", font_big, WHITE, 75)
        screen.blit(font_small.render(f"Sound: {'ON' if settings['sound'] else 'OFF'}", True, WHITE), (80, 140))
        screen.blit(font_small.render(f"Car color: {settings['car_color']}", True, WHITE), (80, 235))
        screen.blit(font_small.render(f"Difficulty: {settings['difficulty']}", True, WHITE), (80, 330))
        for b in [sound_btn, color_btn, diff_btn, back_btn]:
            b.draw()
        for event in pygame.event.get():
            if event.type == QUIT:
                save_settings(settings); pygame.quit(); sys.exit()
            if sound_btn.clicked(event):
                settings["sound"] = not settings["sound"]
                save_settings(settings)
                update_music(settings)
            if color_btn.clicked(event):
                settings["car_color"] = CAR_COLORS[(CAR_COLORS.index(settings["car_color"]) + 1) % len(CAR_COLORS)]
                save_settings(settings)
            if diff_btn.clicked(event):
                settings["difficulty"] = diffs[(diffs.index(settings["difficulty"]) + 1) % len(diffs)]
                save_settings(settings)
            if back_btn.clicked(event):
                return
        pygame.display.update()
        clock.tick(FPS)


def leaderboard_screen(settings):
    back = Button("Back", 120, 525, 160, 40)
    while True:
        update_music(settings)
        screen.fill((25, 25, 25))
        center_text("Top 10", font_big, YELLOW, 60)
        screen.blit(font_tiny.render("Rank  Name        Score   Dist", True, WHITE), (25, 105))
        board = load_leaderboard()
        if not board:
            center_text("No scores yet", font_small, WHITE, 260)
        y = 135
        for i, row in enumerate(board[:10], 1):
            line = f"{i:<5} {row.get('name','Player')[:10]:<10} {row.get('score',0):<7} {row.get('distance',0)}m"
            screen.blit(font_tiny.render(line, True, WHITE), (25, y))
            y += 34
        back.draw()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if back.clicked(event):
                return
        pygame.display.update()
        clock.tick(FPS)


def game_over_screen(name, score, distance, coins, settings):
    # no exit: red background, black GAME OVER, then Retry / Main Menu
    save_score(name, score, distance, coins)
    retry = Button("Retry", 82, 405, 105, 44)
    menu = Button("Main Menu", 205, 405, 115, 44)
    while True:
        update_music(settings)
        screen.fill(RED)
        center_text("GAME OVER", font_big, BLACK, 120)
        center_text(f"Score: {int(score)}", font_small, BLACK, 215)
        center_text(f"Distance: {int(distance)}m", font_small, BLACK, 250)
        center_text(f"Coins: {coins}", font_small, BLACK, 285)
        retry.draw()
        menu.draw()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if retry.clicked(event):
                return "retry"
            if menu.clicked(event):
                return "menu"
        pygame.display.update()
        clock.tick(FPS)



# =====================================================
# 11. MAIN GAME LOOP — main game process
# =====================================================
def play_game(name, settings):
    update_music(settings)
    base_speed = DIFFICULTY[settings["difficulty"]]["speed"]
    spawn_mult = DIFFICULTY[settings["difficulty"]]["spawn_mult"]
    coins_count = 0
    distance = 0.0
    score = 0.0
    active_power = None
    power_end = 0
    shield = False
    repair_charges = 0
    slow_until = 0
    road_scroll = 0

    player = Player(settings["car_color"])
    traffic = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    strips = pygame.sprite.Group()
    player_group = pygame.sprite.Group(player)

    last_traffic = last_coin = last_obstacle = last_power = last_event = pygame.time.get_ticks()

    while True:
        now = pygame.time.get_ticks()
        progress = distance / 600
        speed = base_speed + min(progress * 0.35, 5)
        if active_power == "nitro" and now < power_end:
            speed += 3
        if active_power == "nitro" and now >= power_end:
            active_power = None
        if now < slow_until:
            speed *= 0.55

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return "menu"

        # чем больше progress, тем чаще появляются машины и препятствия
        traffic_interval = max(450, int((1450 - progress * 80) / spawn_mult))
        obstacle_interval = max(650, int((1850 - progress * 90) / spawn_mult))
        if now - last_traffic > traffic_interval:
            traffic.add(TrafficCar(player.rect, random.randint(1, 3)))
            last_traffic = now
        if now - last_coin > 1150:
            coins.add(Coin())
            last_coin = now
        if now - last_obstacle > obstacle_interval:
            obstacles.add(Obstacle(player.rect))
            last_obstacle = now
        if now - last_power > 7000:
            powerups.add(PowerUp())
            last_power = now
        if now - last_event > 9000:
            strips.add(NitroStrip(player.rect))
            last_event = now

        player.move()
        for group in [traffic, coins, obstacles, powerups, strips]:
            for sprite in group:
                sprite.move(speed)

        distance += speed * 0.08
        road_scroll += speed  # faster speed, faster moving bg

        for coin in pygame.sprite.spritecollide(player, coins, True):
            coins_count += coin.value
            # Practice 11 idea: speed rises when coins are collected
            base_speed += 0.04 * coin.value

        for p in pygame.sprite.spritecollide(player, powerups, True):
            if p.kind == "repair":
                repair_charges += 1
                if obstacles:
                    random.choice(obstacles.sprites()).kill()
            elif active_power is None:
                active_power = p.kind
                if p.kind == "nitro":
                    power_end = now + 4000
                elif p.kind == "shield":
                    shield = True

        if pygame.sprite.spritecollide(player, strips, True) and active_power is None:
            active_power = "nitro"
            power_end = now + 3000

        hit_obstacle = pygame.sprite.spritecollideany(player, obstacles)
        if hit_obstacle:
            if hit_obstacle.kind in ["oil", "pothole", "speed_bump"]:
                slow_until = now + 1500
                hit_obstacle.kill()
            elif shield:
                shield = False
                active_power = None
                hit_obstacle.kill()
            elif repair_charges > 0:
                repair_charges -= 1
                hit_obstacle.kill()
            else:
                if settings.get("sound", True) and crash_sound:
                    crash_sound.play()
                return game_over_screen(name, score, distance, coins_count, settings)

        hit_traffic = pygame.sprite.spritecollideany(player, traffic)
        if hit_traffic:
            if shield:
                shield = False
                active_power = None
                hit_traffic.kill()
            elif repair_charges > 0:
                repair_charges -= 1
                hit_traffic.kill()
            else:
                if settings.get("sound", True) and crash_sound:
                    crash_sound.play()
                return game_over_screen(name, score, distance, coins_count, settings)

        # The final score is made up of coins, distance and bonuses
        score = coins_count * 10 + distance + (30 if active_power else 0) + repair_charges * 15
        if distance >= FINISH_DISTANCE:
            save_score(name, score + 500, distance, coins_count)
            return "menu"

        draw_road(road_scroll)
        for group in [strips, coins, powerups, obstacles, traffic, player_group]:
            group.draw(screen)

        remaining = max(0, FINISH_DISTANCE - distance)
        lines = [f"Score: {int(score)}", f"Coins: {coins_count}", f"Distance: {int(distance)}m", f"Remain: {int(remaining)}m", f"Repair: {repair_charges}"]
        y = 8
        for line in lines:
            screen.blit(font_tiny.render(line, True, BLACK), (8, y))
            y += 18
        if active_power == "nitro":
            power_text = f"Power: Nitro {max(0, (power_end - now) // 1000)}s"
        elif active_power == "shield" and shield:
            power_text = "Power: Shield"
        else:
            power_text = "Power: None"
        screen.blit(font_tiny.render(power_text, True, BLACK), (245, 8))

        pygame.display.update()
        clock.tick(FPS)



# =====================================================
# 12. PROGRAM START — main cycle of the programm
# =====================================================
def main():
    settings = load_settings()
    while True:
        action = main_menu(settings)
        if action == "quit":
            pygame.quit(); sys.exit()
        if action == "leaderboard":
            leaderboard_screen(settings)
        elif action == "settings":
            settings_screen(settings)
        elif action == "play":
            player_name = username_screen()
            result = play_game(player_name, settings)
            while result == "retry":
                result = play_game(player_name, settings)


if __name__ == "__main__":
    main()
