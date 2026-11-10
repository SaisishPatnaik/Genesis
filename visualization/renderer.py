
import math
import random
import pygame
import config


class Renderer:
    """
    Fluorescence-microscopy inspired artificial-life renderer.
    Preserves the original visual design and supports research navigation.
    """

    BLACK = (0, 0, 0)
    BLUE = (32, 42, 255)
    VIOLET = (102, 24, 210)
    MAGENTA = (205, 20, 190)
    CYAN = (20, 190, 220)
    GREEN = (45, 205, 75)

    def __init__(self):
        pygame.init()

        self.width = config.WORLD_WIDTH
        self.height = config.WORLD_HEIGHT

        self.screen = pygame.display.set_mode(
            (self.width, self.height),
            pygame.RESIZABLE
        )

        pygame.display.set_caption(config.WINDOW_TITLE)

        self.clock = pygame.time.Clock()
        self.time = 0.0
        self.show_hud = False

        self.font = pygame.font.SysFont("consolas", 14)
        self.small_font = pygame.font.SysFont("consolas", 11)

        self.cell_sprites = {}

        self.background = self._make_background(
            self.width,
            self.height
        )

        self.research_button = pygame.Rect(
            self.width - 215, 15, 195, 38
        )
        self.research_button_hover = False

    def _make_background(self, width, height):
        surface = pygame.Surface((width, height))
        surface.fill(self.BLACK)

        rng = random.Random(6102)

        for _ in range(int(width * height * 0.0012)):
            x = rng.randrange(width)
            y = rng.randrange(height)

            color = rng.choice([
                (2, 2, 7),
                (3, 2, 8),
                (1, 3, 6)
            ])

            surface.set_at((x, y), color)

        return surface

    def _make_cell_sprite(self, organism):
        rng = random.Random(organism.id * 10007 + 31)

        base = rng.randint(56, 86)
        aspect = rng.uniform(0.78, 1.24)

        w = base
        h = int(base * aspect)

        pad = 12
        sw, sh = w + pad * 2, h + pad * 2

        sprite = pygame.Surface((sw, sh), pygame.SRCALPHA)

        cx, cy = sw // 2, sh // 2
        rx, ry = w * 0.47, h * 0.47

        contour = []
        phase = rng.random() * math.tau

        for i in range(96):
            angle = math.tau * i / 96

            wobble = (
                1.0
                + 0.045 * math.sin(3 * angle + phase)
                + 0.028 * math.sin(7 * angle + phase * 1.7)
                + 0.018 * math.sin(11 * angle + phase * 0.4)
            )

            contour.append((
                int(cx + math.cos(angle) * rx * wobble),
                int(cy + math.sin(angle) * ry * wobble)
            ))

        pygame.draw.polygon(
            sprite,
            (26, 15, 105, 58),
            contour
        )

        pygame.draw.lines(
            sprite,
            (48, 35, 190, 85),
            True,
            contour,
            2
        )

        mask = pygame.Surface((sw, sh), pygame.SRCALPHA)

        pygame.draw.polygon(
            mask,
            (255, 255, 255, 255),
            contour
        )

        mask_pixels = pygame.mask.from_surface(mask)

        for _ in range(int(w * h * 0.075)):
            px = rng.randrange(pad, pad + w)
            py = rng.randrange(pad, pad + h)

            if not mask_pixels.get_at((px, py)):
                continue

            choice = rng.random()

            if choice < 0.61:
                color = rng.choice([
                    (27, 38, 210),
                    (42, 35, 235),
                    (65, 28, 180)
                ])
            elif choice < 0.82:
                color = rng.choice([
                    (105, 22, 190),
                    (145, 25, 190),
                    (85, 45, 220)
                ])
            elif choice < 0.94:
                color = rng.choice([
                    (0, 115, 180),
                    (10, 155, 190),
                    (25, 95, 205)
                ])
            else:
                color = rng.choice([
                    (30, 170, 65),
                    (55, 190, 55),
                    (20, 125, 80)
                ])

            radius = rng.choice([1, 1, 1, 2])
            alpha = rng.randint(45, 145)

            pygame.draw.circle(
                sprite,
                (*color, alpha),
                (px, py),
                radius
            )

        for _ in range(rng.randint(5, 10)):
            px = rng.randint(pad + 8, pad + w - 8)
            py = rng.randint(pad + 8, pad + h - 8)

            if mask_pixels.get_at((px, py)):
                color = rng.choice([
                    (40, 30, 170, 20),
                    (100, 15, 150, 24),
                    (0, 80, 160, 20)
                ])

                pygame.draw.circle(
                    sprite,
                    color,
                    (px, py),
                    rng.randint(5, 12)
                )

        nx = cx + rng.randint(
            -int(w * 0.19),
            int(w * 0.19)
        )

        ny = cy + rng.randint(
            -int(h * 0.17),
            int(h * 0.17)
        )

        nr = rng.randint(8, 12)

        pygame.draw.circle(
            sprite,
            (3, 8, 65, 185),
            (nx, ny),
            nr + 2
        )

        pygame.draw.circle(
            sprite,
            (14, 24, 145, 205),
            (nx, ny),
            nr
        )

        pygame.draw.circle(
            sprite,
            (30, 55, 205, 95),
            (nx - 2, ny - 2),
            max(2, nr // 2),
            2
        )

        for _ in range(rng.randint(10, 18)):
            angle = rng.random() * math.tau
            rr = rng.uniform(0.72, 0.98)

            px = int(cx + math.cos(angle) * rx * rr)
            py = int(cy + math.sin(angle) * ry * rr)

            color = rng.choice([
                (30, 160, 225, 130),
                (70, 35, 220, 150),
                (25, 180, 75, 120)
            ])

            pygame.draw.circle(
                sprite,
                color,
                (px, py),
                rng.choice([1, 1, 2])
            )

        return sprite

    def _cell_sprite(self, organism):
        if organism.id not in self.cell_sprites:
            self.cell_sprites[organism.id] = (
                self._make_cell_sprite(organism)
            )

        return self.cell_sprites[organism.id]

    def _draw_background(self):
        self.screen.blit(self.background, (0, 0))

    def _draw_food(self, food, scale_x=1.0, scale_y=1.0):
        for i, (x, y) in enumerate(food):

            if i % 3 == 0:
                color = (15, 95, 170)
            elif i % 3 == 1:
                color = (125, 20, 150)
            else:
                color = (20, 145, 75)

            pulse = 0.65 + 0.35 * math.sin(
                self.time * 1.2 + i
            )

            radius = 1 if pulse < 0.82 else 2

            pygame.draw.circle(
                self.screen,
                color,
                (int(x * scale_x), int(y * scale_y)),
                radius
            )

    def _draw_organism(
        self,
        organism,
        scale_x=1.0,
        scale_y=1.0
    ):
        if not organism.alive:
            return

        sprite = self._cell_sprite(organism)

        shimmer = 0.96 + 0.04 * math.sin(
            self.time * 0.65 + organism.id
        )

        if shimmer < 0.99:
            sprite_to_draw = sprite.copy()
            sprite_to_draw.set_alpha(int(245 * shimmer))
        else:
            sprite_to_draw = sprite

        growth_size = max(
            0.7,
            min(1.8, organism.size)
        )

        # Scale organisms proportionally with the window.
        window_scale = min(scale_x, scale_y)
        final_scale = growth_size * window_scale

        scaled_width = max(
            1,
            int(sprite_to_draw.get_width() * final_scale)
        )

        scaled_height = max(
            1,
            int(sprite_to_draw.get_height() * final_scale)
        )

        scaled_sprite = pygame.transform.smoothscale(
            sprite_to_draw,
            (scaled_width, scaled_height)
        )

        rect = scaled_sprite.get_rect(
            center=(
                int(organism.x * scale_x),
                int(organism.y * scale_y)
            )
        )

        self.screen.blit(scaled_sprite, rect)

    def _draw_research_button(self):
        mouse_pos = pygame.mouse.get_pos()

        self.research_button_hover = (
            self.research_button.collidepoint(mouse_pos)
        )

        bg_color = (
            (24, 35, 75)
            if self.research_button_hover
            else (12, 18, 42)
        )

        border_color = (
            (90, 130, 235)
            if self.research_button_hover
            else (55, 80, 160)
        )

        pygame.draw.rect(
            self.screen,
            bg_color,
            self.research_button,
            border_radius=7
        )

        pygame.draw.rect(
            self.screen,
            border_color,
            self.research_button,
            width=1,
            border_radius=7
        )

        label = self.small_font.render(
            "RESEARCH & ANALYTICS",
            True,
            (155, 185, 255)
        )

        label_rect = label.get_rect(
            center=self.research_button.center
        )

        self.screen.blit(label, label_rect)

    def research_button_clicked(self, event):
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            return self.research_button.collidepoint(event.pos)

        if event.type == pygame.FINGERDOWN:
            x = int(event.x * self.width)
            y = int(event.y * self.height)

            return self.research_button.collidepoint((x, y))

        return False

    def _draw_hud(self, environment, paused, speed):
        if not self.show_hud:
            return

        stats = environment.statistics()

        lines = [
            f"GENESIS  //  {'PAUSED' if paused else 'LIVE'}  //  {speed:.2f}x",
            f"CELLS {stats['population']}   NUTRIENTS {stats['food']}   "
            f"DIVISIONS {stats['births']}   DEATHS {stats['deaths']}",
            f"TIME {environment.elapsed_time:.1f}s   AVG ENERGY {stats['avg_energy']:.1f}",
            "SPACE pause | UP/DOWN speed | TAB hide stats | S export | ESC quit"
        ]

        y = 12

        for i, line in enumerate(lines):
            color = (
                (105, 130, 220)
                if i == 0
                else (95, 95, 145)
            )

            font = self.font if i == 0 else self.small_font

            self.screen.blit(
                font.render(line, True, color),
                (14, y)
            )

            y += 18

    def render(self, environment, paused, simulation_speed):
        self.time = pygame.time.get_ticks() / 1000.0

        # Map the fixed simulation world to the current window.
        scale_x = self.width / environment.width
        scale_y = self.height / environment.height

        self._draw_background()

        self._draw_food(
            environment.food,
            scale_x,
            scale_y
        )

        for organism in environment.organisms:
            self._draw_organism(
                organism,
                scale_x,
                scale_y
            )

        self._draw_hud(
            environment,
            paused,
            simulation_speed
        )

        self._draw_research_button()

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.width, self.height = event.size

            self.screen = pygame.display.set_mode(
                (self.width, self.height),
                pygame.RESIZABLE
            )

            self.background = self._make_background(
                self.width,
                self.height
            )

            self.research_button = pygame.Rect(
                self.width - 215,
                15,
                195,
                38
            )

    def close(self):
        pygame.quit()
