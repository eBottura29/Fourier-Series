import pygame, random, math

from settings import *
from colors import *

# PyGame Setup
pygame.init()

if FULLSCREEN:
    SCREEN = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)
else:
    SCREEN = pygame.display.set_mode(RESOLUTION)

pygame.display.set_caption(WINDOW_NAME)
clock = pygame.time.Clock()
delta_time = 0.01
roboto_big = pygame.font.Font("roboto.ttf", 32)
roboto_small = pygame.font.Font("roboto.ttf", 24)

paused = False

scale_toggle = False

draw_lines = True

scale = 150.0
time_scale = 1.0

drawed_line_width = 5

points = []

speed_ratio = []
length_ratio = []

size = 10

for i in range(size):
    speed_ratio.append(round(random.random(), 2))
    length_ratio.append(round(random.random() / 4 * (1 / size) * 25, 2))


def cartesian_and_polar_conversion(inputs: tuple, operation_index: int):
    output = [0.0, 0.0]

    quadrant = 0

    if inputs[0] >= 0 and inputs[1] >= 0:
        quadrant = 1
    elif inputs[0] < 0 and inputs[1] >= 0:
        quadrant = 2
    elif inputs[0] < 0 and inputs[1] < 0:
        quadrant = 3
    elif inputs[0] >= 0 and inputs[1] < 0:
        quadrant = 4

    if operation_index == 0:
        output[0] = math.sqrt(inputs[0] ** 2 + inputs[1] ** 2)
        output[1] = math.atan(inputs[1] / inputs[0])

        output[1] = math.degrees(output[1])

        if quadrant == 2 or quadrant == 3:
            output[1] += 180
        if quadrant == 4:
            output[1] += 360
    if operation_index == 1:
        output[0] = inputs[0] * math.cos(math.radians(inputs[1]))
        output[1] = inputs[0] * math.sin(math.radians(inputs[1]))

    return tuple(output)


class Text:
    def __init__(
        self,
        text,
        font,
        color,
        position,
        anti_aliasing,
        background=False,
        bg_color=(0, 0, 0),
    ):
        self.text = text
        self.font = font
        self.color = color
        self.position = position
        self.anti_aliasing = anti_aliasing
        self.background = background
        self.bg_color = bg_color

    def draw(self, pos):
        if not self.background:
            self.text = self.font.render(self.text, self.anti_aliasing, self.color)
        elif self.background:
            self.text = self.font.render(
                self.text, self.anti_aliasing, self.color, self.bg_color
            )

        self.text_rect = self.text.get_rect()

        if pos.lower() == "center":
            self.text_rect.center = (self.position[0], self.position[1])
        if pos.lower() == "bottom":
            self.text_rect.bottom = (self.position[0], self.position[1])
        if pos.lower() == "bottomleft":
            self.text_rect.bottomleft = (self.position[0], self.position[1])
        if pos.lower() == "bottomright":
            self.text_rect.bottomright = (self.position[0], self.position[1])
        if pos.lower() == "midbottom":
            self.text_rect.midbottom = (self.position[0], self.position[1])
        if pos.lower() == "midleft":
            self.text_rect.midleft = (self.position[0], self.position[1])
        if pos.lower() == "midright":
            self.text_rect.midright = (self.position[0], self.position[1])
        if pos.lower() == "midtop":
            self.text_rect.midtop = (self.position[0], self.position[1])
        if pos.lower() == "top":
            self.text_rect.top = (self.position[0], self.position[1])
        if pos.lower() == "topleft":
            self.text_rect.topleft = (self.position[0], self.position[1])
        if pos.lower() == "topright":
            self.text_rect.topright = (self.position[0], self.position[1])
        if pos.lower() == "left":
            self.text_rect.left = (self.position[0], self.position[1])
        if pos.lower() == "right":
            self.text_rect.right = (self.position[0], self.position[1])

        SCREEN.blit(self.text, self.text_rect)


class Line:
    def __init__(self, start_pos, length, width, speed, color1, color2):
        self.start_x, self.start_y = start_pos
        self.start_length = length
        self.length = self.start_length
        self.width = width
        self.speed = speed
        self.color1 = color1
        self.color2 = color2

        self.degrees = 0.0

        self.conversion = cartesian_and_polar_conversion((self.length, self.degrees), 1)

        self.end_x = self.conversion[0] + self.start_x
        self.end_y = self.conversion[1] + self.start_y

        self.drawable = False

    def update(self):
        self.degrees += self.speed * time_scale

        self.length = self.start_length * scale

        self.conversion = cartesian_and_polar_conversion((self.length, self.degrees), 1)

        self.end_x = self.conversion[0] + self.start_x
        self.end_y = self.conversion[1] + self.start_y

        if self.drawable:
            points.append((self.end_x, self.end_y))

    def draw(self):
        pygame.draw.line(
            SCREEN,
            self.color1,
            (self.start_x, self.start_y),
            (self.end_x, self.end_y),
            self.width,
        )
        pygame.draw.circle(
            SCREEN, self.color2, (self.end_x, self.end_y), round(self.width * 1.5)
        )


def generate_line_pattern(
    amount_of_lines: int, length_ratio: tuple, speed_ratio: tuple
):
    if (
        len(length_ratio) < amount_of_lines
        or len(length_ratio) > amount_of_lines
        or len(speed_ratio) < amount_of_lines
        or len(speed_ratio) > amount_of_lines
    ):
        raise ValueError("Ratio not the correct size.")

    sticks = []

    last_start_pos = (WIDTH // 2, HEIGHT // 2)

    for i in range(amount_of_lines):
        l = Line(last_start_pos, length_ratio[i], 5, speed_ratio[i], WHITE, RED)
        sticks.append(l)
        last_start_pos = (l.end_x, l.end_y)

    sticks[-1].drawable = True

    return sticks


def draw():
    SCREEN.fill(BLACK)

    for i in range(len(points) - 1):
        pygame.draw.line(SCREEN, WHITE, points[i], points[i + 1], drawed_line_width)

    if draw_lines:
        for line in lines:
            line.draw()

        pygame.draw.circle(SCREEN, RED, (WIDTH // 2, HEIGHT // 2), 10)

        fps_text = Text(
            f"FPS: {round(clock.get_fps(), 2)}", roboto_big, WHITE, (50, 50), True
        )
        fps_text.draw("topleft")

        time_scale_text = Text(
            f"Time Scale: {round(time_scale, 2)}", roboto_big, WHITE, (50, 100), True
        )
        time_scale_text.draw("topleft")

        scale_text = Text(
            f"Scale: {round(scale, 2)}", roboto_big, WHITE, (50, 150), True
        )
        scale_text.draw("topleft")

        length_ratio_text = Text(
            f"Length Ratio: {length_ratio}",
            roboto_small,
            WHITE,
            (WIDTH - 50, HEIGHT - 90),
            True,
        )
        length_ratio_text.draw("bottomright")

        speed_ratio_text = Text(
            f"Speed Ratio: {speed_ratio}",
            roboto_small,
            WHITE,
            (WIDTH - 50, HEIGHT - 50),
            True,
        )
        speed_ratio_text.draw("bottomright")

    pygame.display.flip()


def main():
    global delta_time
    global time_scale
    global paused
    global lines
    global scale_toggle
    global scale
    global points
    global draw_lines

    get_ticks_last_frame = 0

    running = True

    lines = generate_line_pattern(len(length_ratio), length_ratio, speed_ratio)

    temp_time_scale = time_scale

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    paused = not paused
                    if paused:
                        temp_time_scale = time_scale
                        time_scale = 0
                    if not paused:
                        time_scale = temp_time_scale
                if event.key == pygame.K_LSHIFT:
                    draw_lines = not draw_lines
                if event.key == pygame.K_LCTRL:
                    scale_toggle = True
                if event.key == pygame.K_BACKSPACE:
                    points = []
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL:
                    scale_toggle = False
            if event.type == pygame.MOUSEWHEEL:
                paused = False
                if scale_toggle:
                    scale += event.y
                else:
                    time_scale += event.y / 10

        last_start_pos = (WIDTH // 2, HEIGHT // 2)

        for i in range(len(lines)):
            lines[i].start_x, lines[i].start_y = last_start_pos
            last_start_pos = (lines[i].end_x, lines[i].end_y)

        for line in lines:
            line.update()

        draw()
        clock.tick(FPS)

        t = pygame.time.get_ticks()
        delta_time = (t - get_ticks_last_frame) / 1000.0
        get_ticks_last_frame = t

    pygame.quit()


if __name__ == "__main__":
    main()
