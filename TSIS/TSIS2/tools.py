import pygame
import math
from collections import deque

# ============================================================
# TOOLS.PY
# Helper functions for drawing tools and flood-fill.
# This file does not run the game window.
# It only contains reusable drawing logic.
# ============================================================


def rect_from_points(p1, p2):
    """Create a rectangle using two points."""
    x1, y1 = p1
    x2, y2 = p2

    return pygame.Rect(
        min(x1, x2),
        min(y1, y2),
        abs(x2 - x1),
        abs(y2 - y1)
    )


def distance(p1, p2):
    """Calculate distance between two points."""
    return int(math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2))


# ============================================================
# FLOOD FILL TOOL
# ============================================================

def flood_fill(surface, start_pos, fill_color):
    """
    Flood-fill algorithm using pygame.Surface.get_at() and set_at().

    The user clicks inside a closed area.
    The algorithm reads the clicked pixel color and fills all connected
    pixels with the same exact color.
    """
    width, height = surface.get_size()
    start_x, start_y = start_pos

    if not (0 <= start_x < width and 0 <= start_y < height):
        return

    target_color = surface.get_at((start_x, start_y))
    fill_color = pygame.Color(*fill_color)

    if target_color == fill_color:
        return

    queue = deque([(start_x, start_y)])

    while queue:
        x, y = queue.popleft()

        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        if surface.get_at((x, y)) != target_color:
            continue

        surface.set_at((x, y), fill_color)

        queue.append((x + 1, y))
        queue.append((x - 1, y))
        queue.append((x, y + 1))
        queue.append((x, y - 1))


# ============================================================
# BASIC SHAPES
# ============================================================

def draw_rectangle(surface, color, p1, p2, width):
    """Draw a rectangle."""
    pygame.draw.rect(surface, color, rect_from_points(p1, p2), width)


def draw_circle(surface, color, p1, p2, width):
    """Draw a circle. The first point is the center."""
    pygame.draw.circle(surface, color, p1, distance(p1, p2), width)


def draw_line(surface, color, p1, p2, width):
    """Draw a straight line."""
    pygame.draw.line(surface, color, p1, p2, width)


# ============================================================
# PRACTICE 11 SHAPES
# ============================================================

def draw_square(surface, color, p1, p2, width):
    """Draw a square. All sides are equal."""
    x1, y1 = p1
    x2, y2 = p2

    side = max(abs(x2 - x1), abs(y2 - y1))
    dx = side if x2 >= x1 else -side
    dy = side if y2 >= y1 else -side

    rect = pygame.Rect(
        min(x1, x1 + dx),
        min(y1, y1 + dy),
        side,
        side
    )

    pygame.draw.rect(surface, color, rect, width)


def draw_right_triangle(surface, color, p1, p2, width):
    """Draw a right triangle."""
    x1, y1 = p1
    x2, y2 = p2

    points = [
        (x1, y1),
        (x1, y2),
        (x2, y2)
    ]

    pygame.draw.polygon(surface, color, points, width)


def draw_equilateral_triangle(surface, color, p1, p2, width):
    """Draw an equilateral triangle."""
    x1, y1 = p1
    x2, y2 = p2

    side = abs(x2 - x1)
    height = int(side * math.sqrt(3) / 2)
    direction = 1 if y2 >= y1 else -1

    if x2 >= x1:
        points = [
            (x1, y1 + direction * height),
            (x1 + side // 2, y1),
            (x1 + side, y1 + direction * height)
        ]
    else:
        points = [
            (x1, y1 + direction * height),
            (x1 - side // 2, y1),
            (x1 - side, y1 + direction * height)
        ]

    pygame.draw.polygon(surface, color, points, width)


def draw_rhombus(surface, color, p1, p2, width):
    """Draw a rhombus."""
    x1, y1 = p1
    x2, y2 = p2

    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2

    points = [
        (center_x, y1),
        (x2, center_y),
        (center_x, y2),
        (x1, center_y)
    ]

    pygame.draw.polygon(surface, color, points, width)


# ============================================================
# UNIVERSAL SHAPE DISPATCHER
# ============================================================

def draw_selected_shape(surface, tool, color, p1, p2, width):
    """
    Draw the selected tool.
    This function is used both for live preview and final drawing.
    """
    if tool == "line":
        draw_line(surface, color, p1, p2, width)

    elif tool == "rectangle":
        draw_rectangle(surface, color, p1, p2, width)

    elif tool == "circle":
        draw_circle(surface, color, p1, p2, width)

    elif tool == "square":
        draw_square(surface, color, p1, p2, width)

    elif tool == "right_triangle":
        draw_right_triangle(surface, color, p1, p2, width)

    elif tool == "equilateral_triangle":
        draw_equilateral_triangle(surface, color, p1, p2, width)

    elif tool == "rhombus":
        draw_rhombus(surface, color, p1, p2, width)
