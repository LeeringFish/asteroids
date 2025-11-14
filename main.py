import os
os.environ.setdefault("LIBGL_ALWAYS_SOFTWARE", "1")
os.environ.setdefault("SDL_VIDEODRIVER", "x11")
os.environ.setdefault("SDL_VIDEO_X11_FORCE_EGL", "1")

import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from logger import log_state, log_event
from scoremanager import ScoreManager

def new_game():
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    return updatable, drawable, asteroids, shots, player, asteroid_field

def draw_text(surf, msg, size, color, y):
    font = pygame.font.SysFont(None, size)
    img = font.render(msg, True, color)
    rect = img.get_rect(center=(surf.get_width() // 2, y))
    surf.blit(img, rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()
    
    updatable, drawable, asteroids, shots, player, _ = new_game()
    state = "play"
    dt = 0
    score_manager = ScoreManager()
    gameover = False

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if state == "gameover" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    updatable, drawable, asteroids, shots, player, _ = new_game()
                    state = "play"
                    score_manager.current_score = 0
                if event.key == pygame.K_q:
                    return

        screen.fill("black")

        if state == "play":
            updatable.update(dt)

            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    log_event("player_hit")
                    state = "gameover"
                    gameover = False

            for asteroid in asteroids:
                for shot in shots:
                    if shot.collides_with(asteroid):
                        log_event("asteroid_shot")
                        shot.kill()
                        asteroid.split()
                        score_manager.add_point()

            for item in drawable:
                item.draw(screen)
        else:

            if not gameover:
                score = score_manager.current_score

                if score > score_manager.high_score:
                    score_manager.high_score = score
                    score_manager.write_high_score()
                    new_high_score = True
                else:
                    new_high_score = False
                
                gameover = True

            draw_text(screen, "YOU DIED", 72, (255, 70, 70), screen.get_height() // 2 - 40)
            draw_text(screen, "R = Restart Q = Quit", 28, (200, 200, 200), screen.get_height() // 2 + 20)

            if new_high_score:
                draw_text(screen, "New high score!", 28, (200, 200, 200), screen.get_height() // 2 + 70)
                draw_text(screen, f"{score}", 28, (200, 200, 200), screen.get_height() // 2 + 100)
            else:
                draw_text(screen, f"Score: {score}", 28, (200, 200, 200), screen.get_height() // 2 + 70)
                draw_text(screen, f"High score: {score_manager.high_score}", 28, (200, 200, 200), screen.get_height() // 2 + 100)


        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
