from Player import player
from GameObjects.game_object import GameObject, Bullet, ParticleEmitter
import pygame

plr: player.Player
current_level_game_objects: list[GameObject] = []
current_level_bullets: list[Bullet] = []
background_game_object: GameObject
ground_game_object: GameObject

snow: ParticleEmitter = ParticleEmitter()
snow.set_emitter(20, [0, 1964], [-10, -10], [0, -1], 960, 1)

def start_level(level: str) -> None:
    global plr, current_level_game_objects, background_game_object, ground_game_object

    ground_hitbox: GameObject = GameObject()
    ground_hitbox._tag = "ground"
    ground_hitbox.set_position([0, -1080 + 110])
    ground_hitbox._image = pygame.transform.scale(ground_hitbox._image, [1980, 100])
    ground_hitbox._rect = ground_hitbox._image.get_rect()
    current_level_game_objects.append(ground_hitbox)

    ground_game_object = GameObject()
    ground_game_object._tag = "ground_background"
    ground_game_object.set_image("Images/Ground.png")
    ground_game_object.set_position([0, -1080 + 150])
    ground_game_object._image = pygame.transform.scale(ground_game_object._image, [1980, 150])

    background_game_object = GameObject()
    background_game_object._tag = "background"
    background_game_object.set_image("Images/GameBackground_2.png")

    platform_game_object: GameObject = GameObject()
    platform_game_object.set_image("Images/Platform_bush.png")
    platform_game_object.set_position([250, -700])
    current_level_game_objects.append(platform_game_object)

    platform_game_object2: GameObject = GameObject()
    platform_game_object2.set_image("Images/Platform_bush.png")
    platform_game_object2.set_position([750, -700])
    current_level_game_objects.append(platform_game_object2)

    plr = player.Player()
    plr.set_position([10, -800])

def create_bullet(bullet_position: tuple[int, int], bullet_direction: tuple[int, int]) -> None:
    bullet: Bullet = Bullet()
    bullet.set_direction(bullet_direction)
    bullet.set_position(bullet_position)
    current_level_bullets.append(bullet)

def remove_bullet(bullet: Bullet) -> None:
    if bullet in current_level_bullets:
        current_level_bullets.remove(bullet)

def render_level(level: str, screen: pygame.display, delta_time: float) -> None:
    global plr, current_level_game_objects, current_level_bullets, background_game_object, ground_game_object

    background_game_object.render(screen)
    for game_object in current_level_game_objects:
        game_object.render(screen)
    
    for bullet in current_level_bullets:
        bullet.update(delta_time)
        bullet.render(screen)

    if plr._position[1] < -900:
        plr.set_position([0, 0])
    
    if plr._position[0] < 0:
        plr.set_position([0, plr._position[1]])
        plr._dash = 0
    elif plr._position[0] > 1840 - 70:
        plr.set_position([1840 - 70, plr._position[1]])
        plr._dash = 0

    plr.ground_check(current_level_game_objects, delta_time)
    plr.update(delta_time)
    plr.render(screen)

    ParticleEmitter.handle_particle_emmitters(screen)

    ground_game_object.render(screen)

