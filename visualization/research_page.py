
import pygame

from analytics.statistics import research_snapshot


class ResearchPage:

    # --------------------------------------------------
    # VISUAL THEME
    # --------------------------------------------------

    BG = (7, 9, 17)
    PANEL = (15, 19, 34)
    PANEL_HOVER = (23, 29, 52)
    BORDER = (42, 51, 82)

    WHITE = (240, 243, 255)
    MUTED = (155, 166, 195)
    SUBTLE = (112, 126, 158)

    BLUE = (91, 119, 255)
    CYAN = (48, 205, 225)
    PURPLE = (169, 112, 255)
    GREEN = (64, 210, 145)
    RED = (255, 105, 125)
    GOLD = (245, 190, 90)

    def __init__(self):
        pygame.font.init()

        # Stronger, more readable typography.
        self.title_font = pygame.font.SysFont(
            "arial", 34, bold=True
        )

        self.section_font = pygame.font.SysFont(
            "arial", 21, bold=True
        )

        self.heading_font = pygame.font.SysFont(
            "arial", 17, bold=True
        )

        self.metric_font = pygame.font.SysFont(
            "arial", 29, bold=True
        )

        self.body_font = pygame.font.SysFont(
            "arial", 15
        )

        self.body_bold_font = pygame.font.SysFont(
            "arial", 15, bold=True
        )

        self.small_font = pygame.font.SysFont(
            "arial", 13
        )

        self.small_bold_font = pygame.font.SysFont(
            "arial", 13, bold=True
        )

        self.tiny_font = pygame.font.SysFont(
            "arial", 11, bold=True
        )

        self.back_button = pygame.Rect(0, 0, 220, 42)

    # --------------------------------------------------
    # TEXT HELPERS
    # --------------------------------------------------

    def draw_text(
        self,
        screen,
        text,
        x,
        y,
        color=None,
        font=None
    ):
        color = color or self.WHITE
        font = font or self.body_font

        surface = font.render(str(text), True, color)

        screen.blit(
            surface,
            (int(x), int(y))
        )

    def draw_wrapped_text(
        self,
        screen,
        text,
        x,
        y,
        max_width,
        color=None,
        font=None,
        line_spacing=5,
        max_lines=None
    ):
        color = color or self.MUTED
        font = font or self.body_font

        words = str(text).split()
        lines = []
        current_line = ""

        for word in words:
            test_line = (
                word if not current_line
                else current_line + " " + word
            )

            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)

                current_line = word

        if current_line:
            lines.append(current_line)

        if max_lines is not None:
            lines = lines[:max_lines]

        line_height = font.get_linesize() + line_spacing

        for index, line in enumerate(lines):
            self.draw_text(
                screen,
                line,
                x,
                y + index * line_height,
                color,
                font
            )

        return y + len(lines) * line_height

    # --------------------------------------------------
    # PANEL HELPERS
    # --------------------------------------------------

    def draw_panel(
        self,
        screen,
        rect,
        hover=False,
        accent=None
    ):
        if rect.width <= 0 or rect.height <= 0:
            return

        pygame.draw.rect(
            screen,
            self.PANEL_HOVER if hover else self.PANEL,
            rect,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            accent if hover and accent else self.BORDER,
            rect,
            width=1,
            border_radius=10
        )

        if accent and rect.width > 65:
            pygame.draw.line(
                screen,
                accent,
                (rect.x + 14, rect.y + 2),
                (rect.x + 58, rect.y + 2),
                3
            )

    def draw_panel_heading(
        self,
        screen,
        rect,
        heading,
        accent
    ):
        self.draw_text(
            screen,
            heading,
            rect.x + 17,
            rect.y + 13,
            self.WHITE,
            self.heading_font
        )

        pygame.draw.circle(
            screen,
            accent,
            (rect.right - 19, rect.y + 23),
            4
        )

    # --------------------------------------------------
    # HEADER
    # --------------------------------------------------

    def draw_header(self, screen, width, mouse_pos):

        self.draw_text(
            screen,
            "GENESIS",
            25,
            13,
            self.WHITE,
            self.title_font
        )

        title_width = self.title_font.size("GENESIS")[0]

        self.draw_text(
            screen,
            "RESEARCH & ANALYTICS",
            25 + title_width + 22,
            27,
            self.CYAN,
            self.heading_font
        )

        self.draw_text(
            screen,
            "ARTIFICIAL LIFE  /  ECOSYSTEM OBSERVATORY",
            27,
            54,
            self.MUTED,
            self.small_font
        )

        self.back_button = pygame.Rect(
            width - 245,
            17,
            220,
            42
        )

        hover = self.back_button.collidepoint(mouse_pos)

        self.draw_panel(
            screen,
            self.back_button,
            hover,
            self.CYAN
        )

        label = self.body_bold_font.render(
            "BACK TO LIVE SIMULATION",
            True,
            self.CYAN if hover else self.WHITE
        )

        screen.blit(
            label,
            label.get_rect(center=self.back_button.center)
        )

        pygame.draw.line(
            screen,
            self.BORDER,
            (25, 78),
            (width - 25, 78),
            1
        )

    # --------------------------------------------------
    # METRIC CARDS
    # --------------------------------------------------

    def draw_metric(
        self,
        screen,
        rect,
        label,
        value,
        subtitle,
        accent,
        mouse_pos,
        compact=False
    ):
        hover = rect.collidepoint(mouse_pos)

        self.draw_panel(
            screen,
            rect,
            hover,
            accent
        )

        self.draw_text(
            screen,
            label.upper(),
            rect.x + 16,
            rect.y + 11,
            self.MUTED,
            self.tiny_font
        )

        font = (
            self.heading_font
            if compact
            else self.metric_font
        )

        self.draw_text(
            screen,
            value,
            rect.x + 16,
            rect.y + 31 if not compact else rect.y + 29,
            accent if hover else self.WHITE,
            font
        )

        self.draw_text(
            screen,
            subtitle,
            rect.x + 16,
            rect.bottom - 21,
            self.SUBTLE,
            self.small_font
        )

    # --------------------------------------------------
    # ANALYTICS CHARTS
    # --------------------------------------------------

    def draw_chart(
        self,
        screen,
        rect,
        history,
        key,
        heading,
        accent
    ):
        self.draw_panel(screen, rect)

        self.draw_panel_heading(
            screen,
            rect,
            heading,
            accent
        )

        chart = pygame.Rect(
            rect.x + 20,
            rect.y + 49,
            max(1, rect.width - 40),
            max(1, rect.height - 91)
        )

        # Chart grid.
        for i in range(1, 4):
            gy = chart.top + chart.height * i // 4

            pygame.draw.line(
                screen,
                (30, 37, 59),
                (chart.left, gy),
                (chart.right, gy),
                1
            )

        pygame.draw.line(
            screen,
            self.BORDER,
            (chart.left, chart.bottom),
            (chart.right, chart.bottom),
            1
        )

        values = [
            float(item.get(key, 0))
            for item in history
        ]

        if len(values) < 2:
            self.draw_text(
                screen,
                "Collecting ecosystem observations...",
                chart.x + 5,
                chart.y + 15,
                self.MUTED,
                self.small_font
            )
            return

        minimum = min(values)
        maximum = max(values)

        # Avoid a flat line when values are nearly identical.
        if maximum - minimum < 0.0001:
            maximum = minimum + 1.0

        points = []

        for index, value in enumerate(values):
            px = chart.left + (
                index / (len(values) - 1)
            ) * chart.width

            normalized = (
                (value - minimum) / (maximum - minimum)
            )

            py = chart.bottom - normalized * chart.height

            points.append((
                int(px),
                int(py)
            ))

        pygame.draw.lines(
            screen,
            accent,
            False,
            points,
            2
        )

        pygame.draw.circle(
            screen,
            accent,
            points[-1],
            4
        )

        self.draw_text(
            screen,
            f"CURRENT: {values[-1]:.2f}",
            rect.x + 16,
            rect.bottom - 28,
            accent,
            self.small_bold_font
        )

        self.draw_text(
            screen,
            f"MIN {minimum:.2f}",
            rect.right - 155,
            rect.bottom - 28,
            self.SUBTLE,
            self.small_font
        )

    # --------------------------------------------------
    # PROJECT OVERVIEW
    # --------------------------------------------------

    def draw_overview(self, screen, rect, mouse_pos):
        hover = rect.collidepoint(mouse_pos)

        self.draw_panel(
            screen,
            rect,
            hover,
            self.PURPLE
        )

        self.draw_panel_heading(
            screen,
            rect,
            "ABOUT PROJECT GENESIS",
            self.PURPLE
        )

        y = rect.y + 48
        content_width = rect.width - 35

        y = self.draw_wrapped_text(
            screen,
            "Genesis is a computational artificial-life environment "
            "designed to explore how complex population and ecosystem "
            "behaviour can emerge from simple local rules.",
            rect.x + 17,
            y,
            content_width,
            self.MUTED,
            self.body_font
        )

        y += 7

        y = self.draw_wrapped_text(
            screen,
            "Each organism operates independently. It moves through "
            "the environment, searches for nutrients, consumes energy, "
            "grows, and may reproduce when its internal conditions "
            "allow it.",
            rect.x + 17,
            y,
            content_width,
            self.MUTED,
            self.body_font
        )

        y += 7

        self.draw_wrapped_text(
            screen,
            "The simulation records population changes, births, "
            "deaths, organism size and inherited trait variation "
            "to help study the behaviour of the artificial ecosystem.",
            rect.x + 17,
            y,
            content_width,
            self.MUTED,
            self.body_font
        )

    # --------------------------------------------------
    # SIMULATION METHODOLOGY
    # --------------------------------------------------

    def draw_methodology(self, screen, rect, mouse_pos):
        hover = rect.collidepoint(mouse_pos)

        self.draw_panel(
            screen,
            rect,
            hover,
            self.CYAN
        )

        self.draw_panel_heading(
            screen,
            rect,
            "SIMULATION METHODOLOGY",
            self.CYAN
        )

        sections = [
            (
                "01",
                "MOVEMENT",
                "Organisms move directionally and seek nearby food."
            ),
            (
                "02",
                "ENERGY",
                "Movement and survival consume energy; food restores it."
            ),
            (
                "03",
                "GROWTH",
                "Organisms grow when their energy exceeds a threshold."
            ),
            (
                "04",
                "REPRODUCTION",
                "Eligible organisms reproduce asexually and create offspring."
            ),
            (
                "05",
                "INHERITANCE",
                "Offspring inherit parent traits with bounded random mutation."
            ),
            (
                "06",
                "SURVIVAL",
                "Energy depletion and health determine organism survival."
            )
        ]

        available_height = max(50, rect.height - 55)
        spacing = min(
            43,
            available_height / len(sections)
        )

        y = rect.y + 48

        for number, title, description in sections:
            if y + 30 > rect.bottom - 5:
                break

            self.draw_text(
                screen,
                number,
                rect.x + 17,
                int(y),
                self.CYAN,
                self.body_bold_font
            )

            self.draw_text(
                screen,
                title,
                rect.x + 49,
                int(y),
                self.WHITE,
                self.body_bold_font
            )

            if spacing >= 34:
                self.draw_wrapped_text(
                    screen,
                    description,
                    rect.x + 49,
                    int(y + 19),
                    rect.width - 70,
                    self.SUBTLE,
                    self.small_font,
                    line_spacing=2,
                    max_lines=2
                )

            y += spacing

    # --------------------------------------------------
    # RESEARCH OBJECTIVES
    # --------------------------------------------------

    def draw_objectives(self, screen, rect, mouse_pos):
        hover = rect.collidepoint(mouse_pos)

        self.draw_panel(
            screen,
            rect,
            hover,
            self.GREEN
        )

        self.draw_panel_heading(
            screen,
            rect,
            "RESEARCH OBJECTIVES",
            self.GREEN
        )

        objectives = [
            (
                "Population dynamics",
                "Observe how the number of living organisms changes over time."
            ),
            (
                "Resource competition",
                "Examine how limited food resources influence survival."
            ),
            (
                "Generational changes",
                "Track the appearance of new generations through reproduction."
            ),
            (
                "Inherited trait diversity",
                "Observe variation in speed, vision, metabolism and size."
            ),
            (
                "Growth and survival",
                "Study the relationship between energy, growth and mortality."
            )
        ]

        available_height = max(40, rect.height - 55)
        spacing = min(
            39,
            available_height / len(objectives)
        )

        y = rect.y + 48

        for title, description in objectives:
            if y + 18 > rect.bottom - 5:
                break

            pygame.draw.circle(
                screen,
                self.GREEN,
                (rect.x + 21, int(y + 8)),
                4
            )

            self.draw_text(
                screen,
                title,
                rect.x + 35,
                int(y),
                self.WHITE,
                self.body_bold_font
            )

            if spacing >= 33:
                self.draw_wrapped_text(
                    screen,
                    description,
                    rect.x + 35,
                    int(y + 19),
                    rect.width - 55,
                    self.SUBTLE,
                    self.small_font,
                    line_spacing=2,
                    max_lines=2
                )

            y += spacing

    # --------------------------------------------------
    # ECOSYSTEM RULES AND MODEL ASSUMPTIONS
    # --------------------------------------------------

    def draw_ecosystem_rules(self, screen, rect, mouse_pos):
        hover = rect.collidepoint(mouse_pos)

        self.draw_panel(
            screen,
            rect,
            hover,
            self.GOLD
        )

        self.draw_panel_heading(
            screen,
            rect,
            "ECOSYSTEM RULES & MODEL ASSUMPTIONS",
            self.GOLD
        )

        rules = [
            (
                "RESOURCE AVAILABILITY",
                "Food particles are distributed in the environment "
                "and regenerated periodically."
            ),
            (
                "ENERGY DEPENDENCY",
                "Organisms require energy to remain active and reproduce."
            ),
            (
                "POPULATION LIMIT",
                "A maximum population constraint prevents unlimited growth."
            ),
            (
                "TRAIT INHERITANCE",
                "Offspring inherit traits from a single parent with "
                "bounded random variation."
            ),
            (
                "SIMPLIFIED BIOLOGY",
                "Organisms are computational agents, not biological cells."
            )
        ]

        available_height = max(40, rect.height - 55)
        spacing = min(
            40,
            available_height / len(rules)
        )

        y = rect.y + 48

        for title, description in rules:
            if y + 17 > rect.bottom - 5:
                break

            self.draw_text(
                screen,
                title,
                rect.x + 17,
                int(y),
                self.GOLD,
                self.small_bold_font
            )

            if spacing >= 32:
                self.draw_wrapped_text(
                    screen,
                    description,
                    rect.x + 17,
                    int(y + 17),
                    rect.width - 34,
                    self.MUTED,
                    self.small_font,
                    line_spacing=2,
                    max_lines=2
                )

            y += spacing

    # --------------------------------------------------
    # MAIN RENDER
    # --------------------------------------------------

    def render(self, screen, environment):
        width, height = screen.get_size()
        mouse_pos = pygame.mouse.get_pos()

        screen.fill(self.BG)

        stats = research_snapshot(environment)
        history = environment.history

        # Header
        self.draw_header(
            screen,
            width,
            mouse_pos
        )

        # --------------------------------------------------
        # PRIMARY METRICS
        # --------------------------------------------------

        margin = 25
        gap = 12

        card_width = max(
            1,
            (width - margin * 2 - gap * 3) // 4
        )

        primary_metrics = [
            (
                "Population",
                str(stats.get("population", 0)),
                "Living organisms",
                self.GREEN
            ),
            (
                "Births",
                str(stats.get("births", 0)),
                "Total offspring",
                self.CYAN
            ),
            (
                "Deaths",
                str(stats.get("deaths", 0)),
                "Total mortality",
                self.RED
            ),
            (
                "Generation",
                str(stats.get("generations", 0)),
                "Highest living generation",
                self.PURPLE
            )
        ]

        for index, metric in enumerate(primary_metrics):
            x = margin + index * (card_width + gap)

            self.draw_metric(
                screen,
                pygame.Rect(x, 91, card_width, 91),
                *metric,
                mouse_pos
            )

        # --------------------------------------------------
        # SECONDARY METRICS
        # --------------------------------------------------

        secondary_metrics = [
            (
                "Average energy",
                f"{stats.get('avg_energy', 0):.1f}",
                "Energy per organism",
                self.BLUE
            ),
            (
                "Average size",
                f"{stats.get('avg_size', 0):.2f}",
                "Mean organism size",
                self.CYAN
            ),
            (
                "Food available",
                str(stats.get("food", 0)),
                "Current nutrient particles",
                self.GREEN
            ),
            (
                "Genetic diversity",
                f"{stats.get('genetic_diversity', 0):.3f}",
                "Trait variation index",
                self.PURPLE
            )
        ]

        for index, metric in enumerate(secondary_metrics):
            x = margin + index * (card_width + gap)

            self.draw_metric(
                screen,
                pygame.Rect(x, 193, card_width, 76),
                *metric,
                mouse_pos,
                compact=True
            )

        # --------------------------------------------------
        # ANALYTICS CHARTS
        # --------------------------------------------------

        chart_y = 280
        chart_height = max(
            130,
            min(190, int(height * 0.20))
        )

        chart_gap = 14

        chart_width = max(
            1,
            (width - margin * 2 - chart_gap) // 2
        )

        self.draw_chart(
            screen,
            pygame.Rect(
                margin,
                chart_y,
                chart_width,
                chart_height
            ),
            history,
            "population",
            "POPULATION DYNAMICS",
            self.BLUE
        )

        self.draw_chart(
            screen,
            pygame.Rect(
                margin + chart_width + chart_gap,
                chart_y,
                chart_width,
                chart_height
            ),
            history,
            "avg_size",
            "AVERAGE ORGANISM SIZE",
            self.CYAN
        )

        # --------------------------------------------------
        # RESEARCH CONTENT GRID
        # --------------------------------------------------

        lower_y = chart_y + chart_height + 15

        footer_y = height - 31

        lower_height = max(
            100,
            footer_y - lower_y - 13
        )

        column_gap = 14
        row_gap = 12

        available_width = (
            width - margin * 2 - column_gap
        )

        left_width = available_width // 2
        right_width = available_width - left_width

        row_height = max(
            1,
            (lower_height - row_gap) // 2
        )

        left_x = margin
        right_x = margin + left_width + column_gap

        top_rect_left = pygame.Rect(
            left_x,
            lower_y,
            left_width,
            row_height
        )

        top_rect_right = pygame.Rect(
            right_x,
            lower_y,
            right_width,
            row_height
        )

        bottom_rect_left = pygame.Rect(
            left_x,
            lower_y + row_height + row_gap,
            left_width,
            row_height
        )

        bottom_rect_right = pygame.Rect(
            right_x,
            lower_y + row_height + row_gap,
            right_width,
            row_height
        )

        self.draw_overview(
            screen,
            top_rect_left,
            mouse_pos
        )

        self.draw_methodology(
            screen,
            top_rect_right,
            mouse_pos
        )

        self.draw_objectives(
            screen,
            bottom_rect_left,
            mouse_pos
        )

        self.draw_ecosystem_rules(
            screen,
            bottom_rect_right,
            mouse_pos
        )

        # --------------------------------------------------
        # FOOTER
        # --------------------------------------------------

        pygame.draw.line(
            screen,
            self.BORDER,
            (25, footer_y),
            (width - 25, footer_y),
            1
        )

        self.draw_text(
            screen,
            "GENESIS  /  ARTIFICIAL LIFE RESEARCH",
            25,
            height - 23,
            self.MUTED,
            self.tiny_font
        )

        elapsed = stats.get("elapsed_time", 0)

        self.draw_text(
            screen,
            f"SIMULATION TIME: {elapsed:.1f}s",
            width - 205,
            height - 23,
            self.CYAN,
            self.tiny_font
        )

    # --------------------------------------------------
    # BACK BUTTON INPUT
    # --------------------------------------------------

    def back_button_clicked(self, event, screen_size):
        width, height = screen_size

        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            return self.back_button.collidepoint(event.pos)

        if event.type == pygame.FINGERDOWN:
            x = int(event.x * width)
            y = int(event.y * height)

            return self.back_button.collidepoint((x, y))

        return False
