from __future__ import annotations

import json
import os
import random
import sys
from dataclasses import dataclass
from typing import Optional, Tuple

import pygame

from config import *
from db import Database

SETTINGS_FILE = "settings.json"
Vec = Tuple[int, int]


@dataclass
class Food:
    pos: Vec
    color: Tuple[int, int, int]
    points: int
    created_at: int
    lifetime_ms: int = 7000


@dataclass
class PowerUp:
    pos: Vec
    kind: str
    color: Tuple[int, int, int]
    created_at: int
    lifetime_ms: int = 8000


class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("TSIS 4 Snake")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 22)
        self.small_font = pygame.font.SysFont("Arial", 17)
        self.big_font = pygame.font.SysFont("Arial", 42)
        self.db = Database()
        self.settings = self.load_settings()
        self.username = "Player"
        self.personal_best = 0

    def load_settings(self):
        defaults = {"snake_color": [50, 120, 255], "grid_overlay": True, "sound": False}
        if not os.path.exists(SETTINGS_FILE):
            self.save_settings(defaults)
            return defaults
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            defaults.update(data)
        except Exception:
            pass
        return defaults

    def save_settings(self, data=None):
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data or self.settings, f, indent=2)

    def draw_text(self, text, font, color, center=None, pos=None):
        surf = font.render(text, True, color)
        rect = surf.get_rect()
        if center:
            rect.center = center
        elif pos:
            rect.topleft = pos
        self.screen.blit(surf, rect)
        return rect

    def button(self, label, center, w=210, h=42):
        rect = pygame.Rect(0, 0, w, h)
        rect.center = center
        mouse = pygame.mouse.get_pos()
        color = (75, 75, 75) if rect.collidepoint(mouse) else (50, 50, 50)
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        pygame.draw.rect(self.screen, WHITE, rect, 2, border_radius=8)
        self.draw_text(label, self.font, WHITE, center=rect.center)
        return rect

    def main_menu(self):
        while True:
            self.screen.fill(BLACK)
            self.draw_text("SNAKE TSIS 4", self.big_font, GREEN, center=(WIDTH // 2, 55))
            self.draw_text("Username:", self.font, WHITE, center=(WIDTH // 2 - 115, 118))
            input_rect = pygame.Rect(WIDTH // 2 - 55, 98, 220, 42)
            pygame.draw.rect(self.screen, (30, 30, 30), input_rect, border_radius=6)
            pygame.draw.rect(self.screen, WHITE, input_rect, 2, border_radius=6)
            self.draw_text(self.username, self.font, WHITE, pos=(input_rect.x + 10, input_rect.y + 8))

            play = self.button("Play", (WIDTH // 2, 185))
            leaderboard = self.button("Leaderboard", (WIDTH // 2, 240))
            settings = self.button("Settings", (WIDTH // 2, 295))
            quit_btn = self.button("Quit", (WIDTH // 2, 350))
            if not self.db.enabled:
                self.draw_text("DB offline: scores will not be saved", self.small_font, RED, center=(WIDTH // 2, HEIGHT - 25))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1] or ""
                    elif event.key == pygame.K_RETURN:
                        self.personal_best = self.db.get_personal_best(self.username or "Player")
                        return "play"
                    elif len(self.username) < 50 and event.unicode.isprintable():
                        if self.username == "Player":
                            self.username = ""
                        self.username += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if play.collidepoint(event.pos):
                        self.username = self.username.strip() or "Player"
                        self.personal_best = self.db.get_personal_best(self.username)
                        return "play"
                    if leaderboard.collidepoint(event.pos):
                        return "leaderboard"
                    if settings.collidepoint(event.pos):
                        return "settings"
                    if quit_btn.collidepoint(event.pos):
                        self.quit()

    def leaderboard_screen(self):
        while True:
            self.screen.fill(BLACK)
            self.draw_text("LEADERBOARD", self.big_font, YELLOW, center=(WIDTH // 2, 40))
            rows = self.db.get_top_scores(10)
            headers = ["#", "User", "Score", "Lvl", "Date"]
            xs = [25, 70, 250, 340, 410]
            for h, x in zip(headers, xs):
                self.draw_text(h, self.small_font, WHITE, pos=(x, 85))
            y = 115
            if not rows:
                self.draw_text("No DB results yet", self.font, RED, center=(WIDTH // 2, 165))
            for i, (name, score, level, played_at) in enumerate(rows, 1):
                date = played_at.strftime("%Y-%m-%d") if hasattr(played_at, "strftime") else str(played_at)[:10]
                values = [str(i), name[:14], str(score), str(level), date]
                for value, x in zip(values, xs):
                    self.draw_text(value, self.small_font, WHITE, pos=(x, y))
                y += 28
            back = self.button("Back", (WIDTH // 2, HEIGHT - 45))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and back.collidepoint(event.pos):
                    return

    def settings_screen(self):
        colors = [(50, 120, 255), (0, 180, 0), (220, 30, 30), (255, 150, 30), (160, 70, 255)]
        while True:
            self.screen.fill(BLACK)
            self.draw_text("SETTINGS", self.big_font, CYAN, center=(WIDTH // 2, 55))
            grid_btn = self.button(f"Grid: {'ON' if self.settings['grid_overlay'] else 'OFF'}", (WIDTH // 2, 135), 260)
            sound_btn = self.button(f"Sound: {'ON' if self.settings['sound'] else 'OFF'}", (WIDTH // 2, 190), 260)
            self.draw_text("Snake color:", self.font, WHITE, center=(WIDTH // 2, 255))
            color_rects = []
            for i, color in enumerate(colors):
                rect = pygame.Rect(0, 0, 42, 42)
                rect.center = (WIDTH // 2 - 105 + i * 52, 310)
                pygame.draw.rect(self.screen, color, rect, border_radius=6)
                border = 4 if list(color) == self.settings["snake_color"] else 1
                pygame.draw.rect(self.screen, WHITE, rect, border, border_radius=6)
                color_rects.append((rect, color))
            save = self.button("Save & Back", (WIDTH // 2, 380), 260)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.save_settings()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if grid_btn.collidepoint(event.pos):
                        self.settings["grid_overlay"] = not self.settings["grid_overlay"]
                    elif sound_btn.collidepoint(event.pos):
                        self.settings["sound"] = not self.settings["sound"]
                    elif save.collidepoint(event.pos):
                        self.save_settings()
                        return
                    for rect, color in color_rects:
                        if rect.collidepoint(event.pos):
                            self.settings["snake_color"] = list(color)

    def random_free_cell(self, snake, obstacles, *items):
        occupied = set(snake) | set(obstacles)
        for item in items:
            if item is None:
                continue
            if hasattr(item, "pos"):
                occupied.add(item.pos)
            elif isinstance(item, tuple):
                occupied.add(item)
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(1, GRID_HEIGHT - 1))
            if pos not in occupied:
                return pos

    def spawn_food(self, snake, obstacles, poison=None, powerup=None):
        weights = [(10, GREEN), (20, ORANGE), (30, YELLOW)]
        points, color = random.choice(weights)
        return Food(self.random_free_cell(snake, obstacles, poison, powerup), color, points, pygame.time.get_ticks())

    def spawn_poison(self, snake, obstacles, food=None, powerup=None):
        return Food(self.random_free_cell(snake, obstacles, food, powerup), DARK_RED, -1, pygame.time.get_ticks(), 10000)

    def maybe_spawn_powerup(self, snake, obstacles, food=None, poison=None, current=None):
        if current is not None or random.random() > 0.015:
            return current
        kind, color = random.choice([("speed", PURPLE), ("slow", CYAN), ("shield", BLUE)])
        return PowerUp(self.random_free_cell(snake, obstacles, food, poison), kind, color, pygame.time.get_ticks())

    def place_obstacles(self, level, snake, food=None, poison=None, powerup=None):
        if level < 3:
            return set()
        obstacles = set()
        count = min(6 + level * 2, 38)
        head = snake[0]
        safe_zone = {(head[0] + dx, head[1] + dy) for dx in range(-2, 3) for dy in range(-2, 3)}
        attempts = 0
        while len(obstacles) < count and attempts < 1500:
            attempts += 1
            pos = (random.randint(1, GRID_WIDTH - 2), random.randint(2, GRID_HEIGHT - 2))
            if pos in snake or pos in safe_zone or pos in obstacles:
                continue
            if food and pos == food.pos:
                continue
            if poison and pos == poison.pos:
                continue
            if powerup and pos == powerup.pos:
                continue
            trial = obstacles | {pos}
            neighbours = [(head[0] + 1, head[1]), (head[0] - 1, head[1]), (head[0], head[1] + 1), (head[0], head[1] - 1)]
            free_neighbours = [p for p in neighbours if 0 <= p[0] < GRID_WIDTH and 1 <= p[1] < GRID_HEIGHT and p not in trial and p not in snake[1:]]
            if len(free_neighbours) >= 2:
                obstacles.add(pos)
        return obstacles

    def draw_grid(self):
        self.screen.fill(BLACK)
        if self.settings.get("grid_overlay", True):
            for x in range(0, WIDTH, CELL_SIZE):
                pygame.draw.line(self.screen, DARK_GRAY, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, CELL_SIZE):
                pygame.draw.line(self.screen, DARK_GRAY, (0, y), (WIDTH, y))

    def draw_cell(self, pos, color):
        rect = pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, color, rect)

    def draw_info(self, score, level, speed, shield):
        info = f"User: {self.username}  Score: {score}  Level: {level}  Speed: {speed}  Best: {self.personal_best}"
        if shield:
            info += "  Shield: ON"
        self.draw_text(info, self.small_font, WHITE, pos=(8, 4))

    def game_over_screen(self, score, level):
        self.db.save_session(self.username, score, level)
        best_now = max(self.personal_best, self.db.get_personal_best(self.username), score)
        while True:
            self.screen.fill((100, 0, 0))
            self.draw_text("GAME OVER", self.big_font, WHITE, center=(WIDTH // 2, 85))
            self.draw_text(f"Final score: {score}", self.font, WHITE, center=(WIDTH // 2, 150))
            self.draw_text(f"Level reached: {level}", self.font, WHITE, center=(WIDTH // 2, 185))
            self.draw_text(f"Personal best: {best_now}", self.font, WHITE, center=(WIDTH // 2, 220))
            retry = self.button("Retry", (WIDTH // 2, 300))
            menu = self.button("Main Menu", (WIDTH // 2, 355))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return "retry"
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if retry.collidepoint(event.pos):
                        return "retry"
                    if menu.collidepoint(event.pos):
                        return "menu"

    def collision_with_shield(self, shield_active):
        return False if shield_active else True

    def play(self):
        snake = [(5, 5), (4, 5), (3, 5)]
        direction = next_direction = (1, 0)
        score, level, speed, foods_eaten = 0, 1, FPS_START, 0
        obstacles = set()
        food = self.spawn_food(snake, obstacles)
        poison = self.spawn_poison(snake, obstacles, food)
        powerup = None
        speed_effect_until = 0
        speed_delta = 0
        shield = False

        while True:
            now = pygame.time.get_ticks()
            effective_speed = max(3, speed + speed_delta)
            if speed_effect_until and now > speed_effect_until:
                speed_delta = 0
                speed_effect_until = 0
            self.clock.tick(effective_speed)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and direction != (0, 1):
                        next_direction = (0, -1)
                    elif event.key == pygame.K_DOWN and direction != (0, -1):
                        next_direction = (0, 1)
                    elif event.key == pygame.K_LEFT and direction != (1, 0):
                        next_direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                        next_direction = (1, 0)
                    elif event.key == pygame.K_ESCAPE:
                        return "menu"

            if now - food.created_at > food.lifetime_ms:
                food = self.spawn_food(snake, obstacles, poison, powerup)
            if now - poison.created_at > poison.lifetime_ms:
                poison = self.spawn_poison(snake, obstacles, food, powerup)
            if powerup and now - powerup.created_at > powerup.lifetime_ms:
                powerup = None
            powerup = self.maybe_spawn_powerup(snake, obstacles, food, poison, powerup)

            direction = next_direction
            hx, hy = snake[0]
            dx, dy = direction
            new_head = (hx + dx, hy + dy)

            hit_border = not (0 <= new_head[0] < GRID_WIDTH and 1 <= new_head[1] < GRID_HEIGHT)
            hit_self = new_head in snake
            hit_obstacle = new_head in obstacles
            if hit_border or hit_self or hit_obstacle:
                if shield and not hit_obstacle:
                    shield = False
                    new_head = snake[0]
                else:
                    return self.game_over_screen(score, level)

            if new_head != snake[0]:
                snake.insert(0, new_head)
                ate = False
                if new_head == food.pos:
                    score += food.points
                    foods_eaten += 1
                    ate = True
                    food = self.spawn_food(snake, obstacles, poison, powerup)
                    if foods_eaten % LEVEL_UP_EVERY == 0:
                        level += 1
                        speed += 2
                        obstacles = self.place_obstacles(level, snake, food, poison, powerup)
                elif new_head == poison.pos:
                    for _ in range(2):
                        if len(snake) > 0:
                            snake.pop()
                    poison = self.spawn_poison(snake, obstacles, food, powerup)
                    if len(snake) <= 1:
                        return self.game_over_screen(score, level)
                elif powerup and new_head == powerup.pos:
                    if powerup.kind == "speed":
                        speed_delta = 5
                        speed_effect_until = now + 5000
                    elif powerup.kind == "slow":
                        speed_delta = -4
                        speed_effect_until = now + 5000
                    elif powerup.kind == "shield":
                        shield = True
                    powerup = None
                if not ate:
                    snake.pop()

            self.draw_grid()
            for pos in obstacles:
                self.draw_cell(pos, GRAY)
            self.draw_cell(food.pos, food.color)
            self.draw_cell(poison.pos, poison.color)
            if powerup:
                self.draw_cell(powerup.pos, powerup.color)
            for i, pos in enumerate(snake):
                color = tuple(self.settings["snake_color"]) if i == 0 else RED
                self.draw_cell(pos, color)
            self.draw_info(score, level, effective_speed, shield)
            pygame.display.flip()

    def run(self):
        screen_name = "menu"
        while True:
            if screen_name == "menu":
                result = self.main_menu()
                screen_name = result
            elif screen_name == "play":
                result = self.play()
                screen_name = "play" if result == "retry" else "menu"
            elif screen_name == "leaderboard":
                self.leaderboard_screen()
                screen_name = "menu"
            elif screen_name == "settings":
                self.settings_screen()
                screen_name = "menu"

    def quit(self):
        pygame.quit()
        sys.exit()
