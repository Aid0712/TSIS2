import pygame
from collections import deque

# ========================
# Pencil Tool (Freehand)
# ========================
def draw_pencil(surface, color, start_pos, end_pos, size):
    """
    Draw continuous line between two mouse positions.
    Used for smooth freehand drawing.
    """
    pygame.draw.line(surface, color, start_pos, end_pos, size)


# ========================
# Straight Line Tool
# ========================
def draw_line(surface, color, start_pos, end_pos, size):
    pygame.draw.line(surface, color, start_pos, end_pos, size)


# ========================
# Flood Fill (BFS)
# ========================
def flood_fill(surface, x, y, new_color):
    """
    Classic flood fill using BFS (queue).
    
    ⚠ Pitfall:
    - Recursive DFS will crash (stack overflow)
    - Always use queue (BFS)
    """
    width, height = surface.get_size()
    target_color = surface.get_at((x, y))

    if target_color == new_color:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        px, py = queue.popleft()

        if px < 0 or px >= width or py < 0 or py >= height:
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), new_color)

        queue.append((px + 1, py))
        queue.append((px - 1, py))
        queue.append((px, py + 1))
        queue.append((px, py - 1))


# ========================
# Text Tool
# ========================
class TextTool:
    def __init__(self):
        self.active = False
        self.text = ""
        self.position = (0, 0)
        self.font = pygame.font.SysFont(None, 24)

    def start(self, pos):
        self.active = True
        self.text = ""
        self.position = pos

    def handle_event(self, event):
        """
        Handles typing input
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "confirm"
            elif event.key == pygame.K_ESCAPE:
                return "cancel"
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

        return None

    def draw(self, screen):
        """
        Draw preview text (not permanent yet)
        """
        if self.active:
            text_surface = self.font.render(self.text, True, (0, 0, 0))
            screen.blit(text_surface, self.position)

    def render_to_canvas(self, canvas):
        """
        Permanently draw text on canvas
        """
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        canvas.blit(text_surface, self.position)