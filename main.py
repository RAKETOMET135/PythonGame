import pygame
from typing import Final
from Level import level_handler

def render(screen: pygame.display, delta_time: float, level: str) -> None:
    if level_handler.victory_background:
        level_handler.render_victory(screen, delta_time)
    elif level_handler.game_over_background:
        level_handler.render_game_over(screen, delta_time)
    else:
        level_handler.render_level(level, screen, delta_time)

def main() -> None:
    MAX_FRAMERATE: Final[int] = 120

    pygame.init()
    screen: pygame.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock: pygame.time.Clock = pygame.time.Clock()

    delta_time: float = 0
    running: bool = True

    # TODO add level selection
    level: str = "test_level"
    level_handler.start_level(level)

    while running:
        screen.fill("black")

        render(screen, delta_time, level)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        key: pygame.key = pygame.key.get_pressed()

        if key[pygame.K_ESCAPE]:
            running = False
            level_handler.restart_game = False

        pygame.display.flip()

        if level_handler.restart_game:
            pass
            #running = False

        delta_time = clock.tick(MAX_FRAMERATE) / 1000

    pygame.quit()

if __name__ == "__main__":
    main()