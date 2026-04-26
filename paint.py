import pygame
import datetime
from tools import draw_pencil, draw_line, flood_fill, TextTool

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS Paint")

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

clock = pygame.time.Clock()

# ========================
# State
# ========================
color = (0, 0, 0)
brush_size = 2
tool = "pencil"

drawing = False
start_pos = None

text_tool = TextTool()

# ========================
# Main Loop
# ========================
running = True
prev_pos = None

while running:
    screen.fill((200, 200, 200))
    screen.blit(canvas, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ========================
        # Keyboard
        # ========================
        if event.type == pygame.KEYDOWN:

            # Brush size
            if event.key == pygame.K_1:
                brush_size = 2
            elif event.key == pygame.K_2:
                brush_size = 5
            elif event.key == pygame.K_3:
                brush_size = 10

            # Tools
            elif event.key == pygame.K_p:
                tool = "pencil"
            elif event.key == pygame.K_l:
                tool = "line"
            elif event.key == pygame.K_f:
                tool = "fill"
            elif event.key == pygame.K_t:
                tool = "text"

            # Save
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"canvas_{timestamp}.png"
                pygame.image.save(canvas, filename)
                print(f"Saved: {filename}")

        # ========================
        # Mouse
        # ========================
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos
            prev_pos = event.pos

            if tool == "fill":
                flood_fill(canvas, event.pos[0], event.pos[1], color)

            elif tool == "text":
                text_tool.start(event.pos)

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False

            if tool == "line" and start_pos:
                draw_line(canvas, color, start_pos, event.pos, brush_size)

        if event.type == pygame.MOUSEMOTION and drawing:

            if tool == "pencil":
                draw_pencil(canvas, color, prev_pos, event.pos, brush_size)
                prev_pos = event.pos

        # ========================
        # Text tool input
        # ========================
        if text_tool.active:
            result = text_tool.handle_event(event)

            if result == "confirm":
                text_tool.render_to_canvas(canvas)
                text_tool.active = False

            elif result == "cancel":
                text_tool.active = False

    # ========================
    # Line Preview
    # ========================
    if drawing and tool == "line" and start_pos:
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, color, start_pos, mouse_pos, brush_size)

    # ========================
    # Draw text preview
    # ========================
    text_tool.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()