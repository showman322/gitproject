import pygame
from datetime import datetime

from tools import flood_fill, draw_selected_shape

# ============================================================
# PAINT.PY
# Main file of the Paint application.
# It contains pygame initialization, event handling, UI and main loop.
# Drawing algorithms are stored in tools.py.
# ============================================================


# ============================================================
# 1. INITIALIZATION
# ============================================================

pygame.init()

WIDTH, HEIGHT = 800, 600
TOOLBAR_HEIGHT = 60
CANVAS_HEIGHT = HEIGHT - TOOLBAR_HEIGHT
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 2 Paint Application")
clock = pygame.time.Clock()

ui_font = pygame.font.SysFont("Arial", 16)
text_font = pygame.font.SysFont("Arial", 28)


# ============================================================
# 2. COLORS, TOOLS AND GLOBAL STATE
# ============================================================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (225, 225, 225)

COLORS = {
    "Red": (255, 0, 0),
    "Green": (0, 180, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 220, 0),
    "Black": (0, 0, 0),
    "Purple": (160, 70, 220),
}

BRUSH_SIZES = {
    "Small": 2,
    "Medium": 5,
    "Large": 10,
}

current_color = COLORS["Blue"]
current_tool = "pencil"
brush_size = BRUSH_SIZES["Medium"]

drawing = False
start_pos = None
last_pos = None
mouse_pos = None

typing = False
text_position = None
typed_text = ""

saved_message = ""
saved_message_time = 0


# ============================================================
# 3. CANVAS
# ============================================================
# Canvas is separate from the toolbar.
# All drawing is done in canvas coordinates.
# This fixes the bug where shapes appeared lower after release.

canvas = pygame.Surface((WIDTH, CANVAS_HEIGHT))
canvas.fill(WHITE)


# ============================================================
# 4. COORDINATE HELPERS
# ============================================================

def is_on_canvas(screen_pos):
    """Check if mouse position is inside the drawing area."""
    x, y = screen_pos
    return 0 <= x < WIDTH and TOOLBAR_HEIGHT <= y < HEIGHT


def to_canvas_pos(screen_pos):
    """Convert screen coordinates to canvas coordinates."""
    x, y = screen_pos
    return x, y - TOOLBAR_HEIGHT


def to_screen_pos(canvas_pos):
    """Convert canvas coordinates to screen coordinates."""
    x, y = canvas_pos
    return x, y + TOOLBAR_HEIGHT


# ============================================================
# 5. SAVE CANVAS
# ============================================================

def save_canvas():
    """
    Save the canvas as PNG.
    Timestamp in the filename prevents overwriting old images.
    """
    filename = datetime.now().strftime("paint_%Y%m%d_%H%M%S.png")
    pygame.image.save(canvas, filename)
    return filename


# ============================================================
# 6. USER INTERFACE
# ============================================================

def draw_text(surface, text, pos, color=BLACK):
    """Render small UI text."""
    image = ui_font.render(text, True, color)
    surface.blit(image, pos)


def draw_toolbar():
    """Draw toolbar with current tool, brush size, color and shortcuts."""
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))
    pygame.draw.line(screen, BLACK, (0, TOOLBAR_HEIGHT - 1), (WIDTH, TOOLBAR_HEIGHT - 1), 2)

    line1 = (
        f"Tool: {current_tool.upper()} | Size: {brush_size}px | "
        "P Pencil | L Line | R Rect | C Circle | S Square | E Eraser | F Fill | T Text"
    )

    line2 = (
        "Q Right Triangle | W Equilateral Triangle | A Rhombus | "
        "1/2/3 Size | 4-9 Colors | Ctrl+S Save | Space Clear"
    )

    draw_text(screen, line1, (10, 8), BLACK)
    draw_text(screen, line2, (10, 32), BLACK)

    # Current color preview
    pygame.draw.rect(screen, current_color, (WIDTH - 45, 15, 28, 28))
    pygame.draw.rect(screen, BLACK, (WIDTH - 45, 15, 28, 28), 2)

    if saved_message:
        draw_text(screen, saved_message, (WIDTH - 180, 35), (200, 0, 0))


def draw_preview():
    """
    Draw live preview for line and shape tools.
    Preview is drawn on a copy of the canvas, not permanently.
    """
    if not drawing or start_pos is None or mouse_pos is None:
        return

    preview_tools = [
        "line",
        "rectangle",
        "circle",
        "square",
        "right_triangle",
        "equilateral_triangle",
        "rhombus"
    ]

    if current_tool not in preview_tools:
        return

    preview_canvas = canvas.copy()
    draw_selected_shape(preview_canvas, current_tool, current_color, start_pos, mouse_pos, brush_size)
    screen.blit(preview_canvas, (0, TOOLBAR_HEIGHT))


def draw_text_preview():
    """Draw temporary text with cursor before Enter confirms it."""
    if typing and text_position is not None:
        image = text_font.render(typed_text + "|", True, current_color)
        screen.blit(image, to_screen_pos(text_position))


# ============================================================
# 7. KEYBOARD LOGIC
# ============================================================

def handle_keyboard(event):
    """Handle keyboard shortcuts and text tool input."""
    global current_tool, brush_size, current_color
    global typing, typed_text, text_position
    global saved_message, saved_message_time

    # Text tool mode
    if typing:
        if event.key == pygame.K_RETURN:
            canvas.blit(text_font.render(typed_text, True, current_color), text_position)
            typing = False
            typed_text = ""
            text_position = None

        elif event.key == pygame.K_ESCAPE:
            typing = False
            typed_text = ""
            text_position = None

        elif event.key == pygame.K_BACKSPACE:
            typed_text = typed_text[:-1]

        elif event.unicode.isprintable():
            typed_text += event.unicode

        return

    # Ctrl + S saves the canvas
    if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
        filename = save_canvas()
        saved_message = f"Saved: {filename}"
        saved_message_time = pygame.time.get_ticks()
        return

    # Tool shortcuts
    if event.key == pygame.K_p:
        current_tool = "pencil"
    elif event.key == pygame.K_l:
        current_tool = "line"
    elif event.key == pygame.K_r:
        current_tool = "rectangle"
    elif event.key == pygame.K_c:
        current_tool = "circle"
    elif event.key == pygame.K_s:
        current_tool = "square"
    elif event.key == pygame.K_q:
        current_tool = "right_triangle"
    elif event.key == pygame.K_w:
        current_tool = "equilateral_triangle"
    elif event.key == pygame.K_a:
        current_tool = "rhombus"
    elif event.key == pygame.K_e:
        current_tool = "eraser"
    elif event.key == pygame.K_f:
        current_tool = "fill"
    elif event.key == pygame.K_t:
        current_tool = "text"

    # Brush size shortcuts
    elif event.key == pygame.K_1:
        brush_size = BRUSH_SIZES["Small"]
    elif event.key == pygame.K_2:
        brush_size = BRUSH_SIZES["Medium"]
    elif event.key == pygame.K_3:
        brush_size = BRUSH_SIZES["Large"]

    # Color shortcuts
    elif event.key == pygame.K_4:
        current_color = COLORS["Red"]
    elif event.key == pygame.K_5:
        current_color = COLORS["Green"]
    elif event.key == pygame.K_6:
        current_color = COLORS["Blue"]
    elif event.key == pygame.K_7:
        current_color = COLORS["Yellow"]
    elif event.key == pygame.K_8:
        current_color = COLORS["Black"]
    elif event.key == pygame.K_9:
        current_color = COLORS["Purple"]

    # Clear canvas
    elif event.key == pygame.K_SPACE:
        canvas.fill(WHITE)


# ============================================================
# 8. MOUSE LOGIC
# ============================================================

def handle_mouse_down(event):
    """Start drawing, fill an area or start text input."""
    global drawing, start_pos, last_pos, mouse_pos
    global typing, text_position, typed_text

    if not is_on_canvas(event.pos):
        return

    pos = to_canvas_pos(event.pos)

    if event.button == 1:
        if current_tool == "fill":
            flood_fill(canvas, pos, current_color)

        elif current_tool == "text":
            typing = True
            text_position = pos
            typed_text = ""

        else:
            drawing = True
            start_pos = pos
            last_pos = pos
            mouse_pos = pos


def handle_mouse_up(event):
    """Finish drawing a line or a shape."""
    global drawing

    if event.button != 1 or not drawing:
        return

    drawing = False

    if is_on_canvas(event.pos):
        end_pos = to_canvas_pos(event.pos)
    else:
        end_pos = mouse_pos

    if current_tool not in ["pencil", "eraser"]:
        draw_selected_shape(canvas, current_tool, current_color, start_pos, end_pos, brush_size)


def handle_mouse_motion(event):
    """Draw pencil/eraser continuously and update preview position."""
    global last_pos, mouse_pos

    if not is_on_canvas(event.pos):
        return

    mouse_pos = to_canvas_pos(event.pos)

    if drawing:
        if current_tool == "pencil":
            pygame.draw.line(canvas, current_color, last_pos, mouse_pos, brush_size)
            last_pos = mouse_pos

        elif current_tool == "eraser":
            pygame.draw.line(canvas, WHITE, last_pos, mouse_pos, brush_size * 2)
            last_pos = mouse_pos


# ============================================================
# 9. MAIN PROGRAM LOOP
# ============================================================

running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and not typing:
                running = False
            else:
                handle_keyboard(event)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_down(event)

        elif event.type == pygame.MOUSEBUTTONUP:
            handle_mouse_up(event)

        elif event.type == pygame.MOUSEMOTION:
            handle_mouse_motion(event)

    # Hide save message after 1.5 seconds
    if saved_message and pygame.time.get_ticks() - saved_message_time > 1500:
        saved_message = ""

    # Draw everything
    screen.fill(WHITE)
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))
    draw_preview()
    draw_text_preview()
    draw_toolbar()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
