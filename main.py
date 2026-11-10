
import random
import numpy as np
import pygame
import config

from simulation.environment import Environment
from visualization.renderer import Renderer
from visualization.research_page import ResearchPage

from analytics.statistics import (
    export_history,
    research_snapshot
)


def main():
    # Reproducibility
    if config.RANDOM_SEED is not None:
        random.seed(config.RANDOM_SEED)
        np.random.seed(config.RANDOM_SEED)

    # Initialize the shared ecosystem
    environment = Environment()

    # Initialize both application pages
    renderer = Renderer()
    research_page = ResearchPage()

    clock = pygame.time.Clock()

    running = True
    paused = False

    simulation_speed = config.SIMULATION_SPEED

    # Genesis always opens on the live simulation
    current_page = "LIVE"

    print("PROJECT GENESIS — ARTIFICIAL LIFE SIMULATION")
    print("---------------------------------------------")
    print("LIVE PAGE:")
    print("Research button: Open research and analytics")
    print("SPACE: Pause / Resume")
    print("UP/DOWN: Change simulation speed")
    print("TAB: Toggle simulation HUD")
    print("S: Export analytics")
    print()
    print("RESEARCH PAGE:")
    print("Back button: Return to live simulation")
    print("R: Switch between pages")
    print()
    print("ESC / Q: Exit Genesis")

    # Main application loop
    while running:

        frame_dt = clock.tick(config.FPS) / 1000.0

        for event in pygame.event.get():

            # Handle window events
            renderer.handle_event(event)

            # Window close
            if event.type == pygame.QUIT:
                running = False
                continue

            # ------------------------------------------
            # LIVE PAGE NAVIGATION
            # ------------------------------------------

            if (
                current_page == "LIVE"
                and renderer.research_button_clicked(event)
            ):
                current_page = "RESEARCH"
                continue

            # ------------------------------------------
            # RESEARCH PAGE NAVIGATION
            # ------------------------------------------

            if (
                current_page == "RESEARCH"
                and research_page.back_button_clicked(
                    event,
                    renderer.screen.get_size()
                )
            ):
                current_page = "LIVE"
                continue

            # ------------------------------------------
            # KEYBOARD CONTROLS
            # ------------------------------------------

            if event.type == pygame.KEYDOWN:

                # Exit application
                if event.key in (
                    pygame.K_ESCAPE,
                    pygame.K_q
                ):
                    running = False

                # Switch pages
                elif event.key == pygame.K_r:

                    if current_page == "LIVE":
                        current_page = "RESEARCH"
                    else:
                        current_page = "LIVE"

                # Pause / resume
                elif event.key == pygame.K_SPACE:
                    paused = not paused

                # Increase simulation speed
                elif event.key == pygame.K_UP:
                    simulation_speed = min(
                        simulation_speed + config.SPEED_INCREMENT,
                        config.MAX_SIMULATION_SPEED
                    )

                # Decrease simulation speed
                elif event.key == pygame.K_DOWN:
                    simulation_speed = max(
                        simulation_speed - config.SPEED_INCREMENT,
                        config.MIN_SIMULATION_SPEED
                    )

                # Toggle HUD on live page
                elif (
                    event.key == pygame.K_TAB
                    and current_page == "LIVE"
                ):
                    renderer.show_hud = not renderer.show_hud

                # Export analytics
                elif event.key == pygame.K_s:

                    path = export_history(environment)

                    print(
                        f"Analytics exported to: {path.resolve()}"
                    )

                    print(
                        "Research snapshot:",
                        research_snapshot(environment)
                    )

        # ----------------------------------------------
        # UPDATE SHARED ECOSYSTEM
        # ----------------------------------------------

        # The same environment continues running
        # regardless of which page is currently visible.

        if not paused:
            environment.update(
                frame_dt * simulation_speed
            )

        # ----------------------------------------------
        # PAGE RENDERING
        # ----------------------------------------------

        if current_page == "LIVE":

            renderer.render(
                environment,
                paused,
                simulation_speed
            )

        elif current_page == "RESEARCH":

            research_page.render(
                renderer.screen,
                environment
            )

            pygame.display.flip()

    # ----------------------------------------------
    # SHUTDOWN
    # ----------------------------------------------

    renderer.close()

    print("PROJECT GENESIS — SIMULATION CLOSED")


if __name__ == "__main__":
    main()
