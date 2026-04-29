from __future__ import annotations  # Allows using type annotations in a more flexible way

import json  # Used to load and save settings in JSON format
import os  # Used to check if the settings file exists
import random  # Used for random food, poison, power-up, and obstacle positions
import sys  # Used to close the program completely
from dataclasses import dataclass  # Used to create simple data classes
from typing import Optional, Tuple  # Used for type hints

import pygame  

from config import *  # Imports constants such as WIDTH, HEIGHT, colors, FPS, grid size
from db import Database  # Imports database class for saving and loading scores

SETTINGS_FILE = "settings.json"  # File where game settings are stored
Vec = Tuple[int, int]  # Type alias for grid position, for example (x, y)


@dataclass
class Food:
    # This class stores information about food or poison on the field
    pos: Vec  # Position of the food on the grid
    color: Tuple[int, int, int]  # RGB color of the food
    points: int  # Points given when snake eats it
    created_at: int  # Time when this food was created
    lifetime_ms: int = 7000  # How long the food exists before respawning


@dataclass
class PowerUp:
    # This class stores information about power-ups
    pos: Vec  # Position of the power-up on the grid
    kind: str  # Type of power-up: speed, slow, or shield
    color: Tuple[int, int, int]  # RGB color of the power-up
    created_at: int  # Time when this power-up was created
    lifetime_ms: int = 8000  # How long the power-up exists before disappearing


class SnakeGame:
    def __init__(self):
        # This constructor initializes the whole game
        pygame.init()  # Starts pygame modules
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
        # This function loads settings from settings.json
        defaults = {"snake_color": [50, 120, 255], "grid_overlay": True, "sound": False}  # Default settings

        # If settings file does not exist, create it with default values
        if not os.path.exists(SETTINGS_FILE):
            self.save_settings(defaults)
            return defaults

        try:
            # Open settings file and read JSON data
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Update default settings with saved user settings
            defaults.update(data)
        except Exception:
            # If file is damaged or cannot be read, ignore error and use defaults
            pass

        return defaults  # Return final settings

    def save_settings(self, data=None):
        # This function saves settings to settings.json
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data or self.settings, f, indent=2)

    def draw_text(self, text, font, color, center=None, pos=None):
        # This function draws text on the screen
        surf = font.render(text, True, color)  # Creates text surface
        rect = surf.get_rect()  # Gets rectangle of the text surface

        # If center is given, place text by center
        if center:
            rect.center = center

        # If pos is given, place text by top-left position
        elif pos:
            rect.topleft = pos

        self.screen.blit(surf, rect)  # Draw text on the screen
        return rect  # Return rectangle, useful for buttons/collisions

    def button(self, label, center, w=210, h=42):
        # This function creates and draws a clickable button
        rect = pygame.Rect(0, 0, w, h)  # Create rectangle for button
        rect.center = center  # Put button in the needed center position
        mouse = pygame.mouse.get_pos()  # Get mouse position

        # If mouse is over the button, make it lighter
        color = (75, 75, 75) if rect.collidepoint(mouse) else (50, 50, 50)

        pygame.draw.rect(self.screen, color, rect, border_radius=8)  # Draw button background
        pygame.draw.rect(self.screen, WHITE, rect, 2, border_radius=8)  # Draw white border
        self.draw_text(label, self.font, WHITE, center=rect.center)  # Draw button text
        return rect  # Return button rectangle to check mouse clicks

    def main_menu(self):
        # This function shows the main menu
        while True:
            self.screen.fill(BLACK)  # Clear screen with black color

            # Draw game title
            self.draw_text("SNAKE TSIS 4", self.big_font, GREEN, center=(WIDTH // 2, 55))

            # Draw username label
            self.draw_text("Username:", self.font, WHITE, center=(WIDTH // 2 - 115, 118))

            # Create input rectangle for username
            input_rect = pygame.Rect(WIDTH // 2 - 55, 98, 220, 42)
            pygame.draw.rect(self.screen, (30, 30, 30), input_rect, border_radius=6)
            pygame.draw.rect(self.screen, WHITE, input_rect, 2, border_radius=6)

            # Draw current username inside input field
            self.draw_text(self.username, self.font, WHITE, pos=(input_rect.x + 10, input_rect.y + 8))

            # Create menu buttons
            play = self.button("Play", (WIDTH // 2, 185))
            leaderboard = self.button("Leaderboard", (WIDTH // 2, 240))
            settings = self.button("Settings", (WIDTH // 2, 295))
            quit_btn = self.button("Quit", (WIDTH // 2, 350))

            # If database is disabled, show warning
            if not self.db.enabled:
                self.draw_text("DB offline: scores will not be saved", self.small_font, RED, center=(WIDTH // 2, HEIGHT - 25))

            pygame.display.flip()  # Update screen

            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                # Keyboard handling for username input and Enter
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

                # Mouse click handling
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
        # This function shows leaderboard screen with top scores
        while True:
            self.screen.fill(BLACK)  # Clear screen
            self.draw_text("LEADERBOARD", self.big_font, YELLOW, center=(WIDTH // 2, 40))  # Title

            rows = self.db.get_top_scores(10)  # Get top 10 results from database

            headers = ["#", "User", "Score", "Lvl", "Date"]  # Table headers
            xs = [25, 70, 250, 340, 410]  # X positions for table columns

            # Draw table headers
            for h, x in zip(headers, xs):
                self.draw_text(h, self.small_font, WHITE, pos=(x, 85))

            y = 115  # First row Y position

            # If no records found, show message
            if not rows:
                self.draw_text("No DB results yet", self.font, RED, center=(WIDTH // 2, 165))

            # Draw every score row
            for i, (name, score, level, played_at) in enumerate(rows, 1):
                date = played_at.strftime("%Y-%m-%d") if hasattr(played_at, "strftime") else str(played_at)[:10]
                values = [str(i), name[:14], str(score), str(level), date]

                # Draw each column value
                for value, x in zip(values, xs):
                    self.draw_text(value, self.small_font, WHITE, pos=(x, y))

                y += 28  # Move to next row

            back = self.button("Back", (WIDTH // 2, HEIGHT - 45))  # Back button
            pygame.display.flip()  # Update screen

            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and back.collidepoint(event.pos):
                    return

    def settings_screen(self):
        # This function shows settings screen
        colors = [(50, 120, 255), (0, 180, 0), (220, 30, 30), (255, 150, 30), (160, 70, 255)]  # Available snake colors

        while True:
            self.screen.fill(BLACK)  # Clear screen
            self.draw_text("SETTINGS", self.big_font, CYAN, center=(WIDTH // 2, 55))  # Title

            # Buttons for grid and sound settings
            grid_btn = self.button(f"Grid: {'ON' if self.settings['grid_overlay'] else 'OFF'}", (WIDTH // 2, 135), 260)
            sound_btn = self.button(f"Sound: {'ON' if self.settings['sound'] else 'OFF'}", (WIDTH // 2, 190), 260)

            # Color selection label
            self.draw_text("Snake color:", self.font, WHITE, center=(WIDTH // 2, 255))

            color_rects = []  # Stores rectangles for color buttons

            # Draw color buttons
            for i, color in enumerate(colors):
                rect = pygame.Rect(0, 0, 42, 42)
                rect.center = (WIDTH // 2 - 105 + i * 52, 310)
                pygame.draw.rect(self.screen, color, rect, border_radius=6)

                # If this color is selected, draw thicker border
                border = 4 if list(color) == self.settings["snake_color"] else 1
                pygame.draw.rect(self.screen, WHITE, rect, border, border_radius=6)

                color_rects.append((rect, color))

            save = self.button("Save & Back", (WIDTH // 2, 380), 260)  # Save button
            pygame.display.flip()  # Update screen

            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                # Escape saves settings and returns
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.save_settings()
                    return

                # Mouse clicks on settings buttons
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if grid_btn.collidepoint(event.pos):
                        self.settings["grid_overlay"] = not self.settings["grid_overlay"]
                    elif sound_btn.collidepoint(event.pos):
                        self.settings["sound"] = not self.settings["sound"]
                    elif save.collidepoint(event.pos):
                        self.save_settings()
                        return

                    # Change snake color if user clicked a color square
                    for rect, color in color_rects:
                        if rect.collidepoint(event.pos):
                            self.settings["snake_color"] = list(color)

    def random_free_cell(self, snake, obstacles, *items):
        # This function finds a random empty cell on the grid
        occupied = set(snake) | set(obstacles)  # Cells already occupied by snake or obstacles

        # Add positions of food, poison, or power-ups to occupied cells
        for item in items:
            if item is None:
                continue
            if hasattr(item, "pos"):
                occupied.add(item.pos)
            elif isinstance(item, tuple):
                occupied.add(item)

        # Generate random cells until a free one is found
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(1, GRID_HEIGHT - 1))
            if pos not in occupied:
                return pos

    def spawn_food(self, snake, obstacles, poison=None, powerup=None):
        # This function creates normal food
        weights = [(10, GREEN), (20, ORANGE), (30, YELLOW)]  # Different food types with different points
        points, color = random.choice(weights)  # Choose random food type
        return Food(self.random_free_cell(snake, obstacles, poison, powerup), color, points, pygame.time.get_ticks())

    def spawn_poison(self, snake, obstacles, food=None, powerup=None):
        # This function creates poison
        return Food(self.random_free_cell(snake, obstacles, food, powerup), DARK_RED, -1, pygame.time.get_ticks(), 10000)

    def maybe_spawn_powerup(self, snake, obstacles, food=None, poison=None, current=None):
        # This function randomly creates a power-up
        if current is not None or random.random() > 0.015:
            return current

        # Choose random power-up type
        kind, color = random.choice([("speed", PURPLE), ("slow", CYAN), ("shield", BLUE)])
        return PowerUp(self.random_free_cell(snake, obstacles, food, poison), kind, color, pygame.time.get_ticks())

    def place_obstacles(self, level, snake, food=None, poison=None, powerup=None):
        # This function places obstacles starting from level 3
        if level < 3:
            return set()

        obstacles = set()  # Stores obstacle positions
        count = min(6 + level * 2, 38)  # Number of obstacles, limited to 38
        head = snake[0]  # Snake head position

        # Safe area around snake head so player is not blocked immediately
        safe_zone = {(head[0] + dx, head[1] + dy) for dx in range(-2, 3) for dy in range(-2, 3)}

        attempts = 0  # Prevents infinite loop

        # Try to place obstacles
        while len(obstacles) < count and attempts < 1500:
            attempts += 1
            pos = (random.randint(1, GRID_WIDTH - 2), random.randint(2, GRID_HEIGHT - 2))

            # Skip if position is not allowed
            if pos in snake or pos in safe_zone or pos in obstacles:
                continue
            if food and pos == food.pos:
                continue
            if poison and pos == poison.pos:
                continue
            if powerup and pos == powerup.pos:
                continue

            trial = obstacles | {pos}  # Test obstacle set

            # Check cells near snake head
            neighbours = [(head[0] + 1, head[1]), (head[0] - 1, head[1]), (head[0], head[1] + 1), (head[0], head[1] - 1)]

            # Count free neighbouring cells
            free_neighbours = [p for p in neighbours if 0 <= p[0] < GRID_WIDTH and 1 <= p[1] < GRID_HEIGHT and p not in trial and p not in snake[1:]]

            # Add obstacle only if snake still has at least two possible moves
            if len(free_neighbours) >= 2:
                obstacles.add(pos)

        return obstacles

    def draw_grid(self):
        # This function draws the background and grid
        self.screen.fill(BLACK)

        # Draw grid only if setting is enabled
        if self.settings.get("grid_overlay", True):
            for x in range(0, WIDTH, CELL_SIZE):
                pygame.draw.line(self.screen, DARK_GRAY, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, CELL_SIZE):
                pygame.draw.line(self.screen, DARK_GRAY, (0, y), (WIDTH, y))

    def draw_cell(self, pos, color):
        # This function draws one cell on the grid
        rect = pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, color, rect)

    def draw_info(self, score, level, speed, shield):
        # This function draws game information at the top
        info = f"User: {self.username}  Score: {score}  Level: {level}  Speed: {speed}  Best: {self.personal_best}"

        # Add shield information if shield is active
        if shield:
            info += "  Shield: ON"

        self.draw_text(info, self.small_font, WHITE, pos=(8, 4))

    def game_over_screen(self, score, level):
        # This function shows game over screen
        self.db.save_session(self.username, score, level)  # Save result to database
        best_now = max(self.personal_best, self.db.get_personal_best(self.username), score)  # Calculate best score

        while True:
            self.screen.fill((100, 0, 0))  # Red background
            self.draw_text("GAME OVER", self.big_font, WHITE, center=(WIDTH // 2, 85))
            self.draw_text(f"Final score: {score}", self.font, WHITE, center=(WIDTH // 2, 150))
            self.draw_text(f"Level reached: {level}", self.font, WHITE, center=(WIDTH // 2, 185))
            self.draw_text(f"Personal best: {best_now}", self.font, WHITE, center=(WIDTH // 2, 220))

            # Buttons
            retry = self.button("Retry", (WIDTH // 2, 300))
            menu = self.button("Main Menu", (WIDTH // 2, 355))

            pygame.display.flip()  # Update screen

            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                # Keyboard controls
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return "retry"
                    if event.key == pygame.K_ESCAPE:
                        return "menu"

                # Mouse controls
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if retry.collidepoint(event.pos):
                        return "retry"
                    if menu.collidepoint(event.pos):
                        return "menu"

    def collision_with_shield(self, shield_active):
        # This function returns collision result depending on shield
        return False if shield_active else True

    def play(self):
        # This is the main game loop
        snake = [(5, 5), (4, 5), (3, 5)]  # Starting snake body
        direction = next_direction = (1, 0)  # Initial movement direction: right
        score, level, speed, foods_eaten = 0, 1, FPS_START, 0  # Game stats
        obstacles = set()  # Obstacles on the map
        food = self.spawn_food(snake, obstacles)  # Create first food
        poison = self.spawn_poison(snake, obstacles, food)  # Create first poison
        powerup = None  # No power-up at start
        speed_effect_until = 0  # Time until speed effect ends
        speed_delta = 0  # Temporary speed change
        shield = False  # Shield is off at start

        while True:
            now = pygame.time.get_ticks()  # Current game time
            effective_speed = max(3, speed + speed_delta)  # Calculate current speed, minimum 3

            # If speed effect time is over, reset speed effect
            if speed_effect_until and now > speed_effect_until:
                speed_delta = 0
                speed_effect_until = 0

            self.clock.tick(effective_speed)  # Control game FPS

            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                # Keyboard movement
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

            # Respawn food if its lifetime expired
            if now - food.created_at > food.lifetime_ms:
                food = self.spawn_food(snake, obstacles, poison, powerup)

            # Respawn poison if its lifetime expired
            if now - poison.created_at > poison.lifetime_ms:
                poison = self.spawn_poison(snake, obstacles, food, powerup)

            # Remove power-up if lifetime expired
            if powerup and now - powerup.created_at > powerup.lifetime_ms:
                powerup = None

            # Maybe spawn new power-up
            powerup = self.maybe_spawn_powerup(snake, obstacles, food, poison, powerup)

            direction = next_direction  # Apply next direction
            hx, hy = snake[0]  # Current head position
            dx, dy = direction  # Direction values
            new_head = (hx + dx, hy + dy)  # New head position

            # Check collisions
            hit_border = not (0 <= new_head[0] < GRID_WIDTH and 1 <= new_head[1] < GRID_HEIGHT)
            hit_self = new_head in snake
            hit_obstacle = new_head in obstacles

            # If collision happens
            if hit_border or hit_self or hit_obstacle:
                # Shield protects from border/self collision, but not from obstacle
                if shield and not hit_obstacle:
                    shield = False
                    new_head = snake[0]
                else:
                    return self.game_over_screen(score, level)

            # Move snake only if head actually changed
            if new_head != snake[0]:
                snake.insert(0, new_head)  # Add new head
                ate = False  # Shows if snake ate normal food

                # If snake eats food
                if new_head == food.pos:
                    score += food.points  # Add points
                    foods_eaten += 1  # Count eaten food
                    ate = True
                    food = self.spawn_food(snake, obstacles, poison, powerup)  # Spawn new food

                    # Level up after specific number of foods
                    if foods_eaten % LEVEL_UP_EVERY == 0:
                        level += 1
                        speed += 2
                        obstacles = self.place_obstacles(level, snake, food, poison, powerup)

                # If snake eats poison
                elif new_head == poison.pos:
                    # Remove two parts of snake
                    for _ in range(2):
                        if len(snake) > 0:
                            snake.pop()

                    poison = self.spawn_poison(snake, obstacles, food, powerup)  # Spawn new poison

                    # If snake becomes too short, game over
                    if len(snake) <= 1:
                        return self.game_over_screen(score, level)

                # If snake takes power-up
                elif powerup and new_head == powerup.pos:
                    if powerup.kind == "speed":
                        speed_delta = 5
                        speed_effect_until = now + 5000
                    elif powerup.kind == "slow":
                        speed_delta = -4
                        speed_effect_until = now + 5000
                    elif powerup.kind == "shield":
                        shield = True

                    powerup = None  # Remove collected power-up

                # If snake did not eat food, remove tail to keep same length
                if not ate:
                    snake.pop()

            # Draw everything
            self.draw_grid()

            # Draw obstacles
            for pos in obstacles:
                self.draw_cell(pos, GRAY)

            # Draw food and poison
            self.draw_cell(food.pos, food.color)
            self.draw_cell(poison.pos, poison.color)

            # Draw power-up if it exists
            if powerup:
                self.draw_cell(powerup.pos, powerup.color)

            # Draw snake
            for i, pos in enumerate(snake):
                color = tuple(self.settings["snake_color"]) if i == 0 else RED
                self.draw_cell(pos, color)

            # Draw information bar
            self.draw_info(score, level, effective_speed, shield)

            pygame.display.flip()  # Update display

    def run(self):
        # This function controls screen switching
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
        # This function closes pygame and exits program
        pygame.quit()
        sys.exit()