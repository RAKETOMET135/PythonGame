from Player import player
from GameObjects.game_object import GameObject, Bullet, ParticleEmitter, Boss
import pygame, random

plr: player.Player
current_level_game_objects: list[GameObject] = []
current_level_bullets: list[Bullet] = []
current_level_targets: list = []
tracked_carrots: list[GameObject] = []
carrot_track_delay: float = 0
cloud: GameObject = None
lightnings: list[GameObject] = []
candy_canes: list[GameObject] = []
background_game_object: GameObject
ground_game_object: GameObject

snow: ParticleEmitter = ParticleEmitter()
snow.set_emitter(20, (0, 1964), (-10, -10), [(0, -1)], 960, 1, True, (-1, 1, -2, -1))
snow.set_particle_image("Images/SnowParticle.png")

boss: Boss = Boss(600)
boss.set_position([1450, -350])
current_level_targets.append(boss)

def add_level_target(target) -> None:
    current_level_targets.append(target)

    for bullet in current_level_bullets:
        bullet.set_targets(current_level_targets)

def remove_tracked_carrot(carrot: GameObject) -> None:
    global tracked_carrots

    if carrot in tracked_carrots:
        tracked_carrots.remove(carrot)
        current_level_targets.remove(carrot)

        del carrot
    
    for bullet in current_level_bullets:
        bullet.set_targets(current_level_targets)

def create_tracked_carrot() -> None:
    global tracked_carrots

    tracked_carrot: GameObject = GameObject()
    tracked_carrot.set_position((1450+107, -525))
    tracked_carrot.set_image("Images/Carrot.png")
    tracked_carrot._parameter = 5
    add_level_target(tracked_carrot)
    
    tracked_carrots.append(tracked_carrot)

def track_carrot(carrot: GameObject, delta_time: float, delay: float) -> None:
    global plr

    if delay <= 0:
        x_multi: int = -1
        y_multi: int = 1

        if carrot._position[0] < plr._position[0]:
            x_multi = 1
    
        if carrot._position[1] > plr._position[1]:
            y_multi = -1

        carrot._velocity = [random.randint(1, 3), random.randint(1, 3)]

        new_position: tuple[int, int] = (carrot._position[0] + carrot._velocity[0] * x_multi * delta_time * 100, carrot._position[1] + carrot._velocity[1] * y_multi * delta_time * 100)
        carrot.set_position(new_position)
        carrot._direction = [x_multi, y_multi]
    else:
        new_position: tuple[int, int] = (carrot._position[0] + carrot._velocity[0] * carrot._direction[0] * delta_time * 100, carrot._position[1] + carrot._velocity[1] * carrot._direction[1] * delta_time * 100)
        carrot.set_position(new_position)

total_l: int = 0
def create_cloud() -> None:
    global cloud, total_l

    if cloud:
        total_l = 0
    else:
        cloud = GameObject()
        cloud.set_position((75, -50))
        cloud.set_image("Images/Cloud.png")

def handle_cloud(delta_time: float) -> None:
    global cloud, plr, lightnings, total_l

    move_x: int = -1

    if cloud._position[0] < plr._position[0]:
        move_x = 1
    
    cloud._parameter += 1 * delta_time * 100

    if abs(cloud._position[0] - plr._position[0]) < 10:
        move_x = 0

    if cloud._parameter > 250:
        lightning: GameObject = GameObject()
        lightning.set_image("Images/Lightning.png")
        lightning.set_position((cloud._position[0] +100, cloud._position[1] - 75))
        lightnings.append(lightning)
        cloud._parameter = 0
        total_l += 1

        if total_l > 5:
            total_l = 0
            del cloud
            cloud = None
            return

    cloud.set_position([cloud._position[0] + 3 * move_x * delta_time * 100, cloud._position[1]])

def update_lightning(lightning: GameObject, delta_time: float) -> None:
    global lightnings

    lightning.set_position((lightning._position[0], lightning._position[1] - 10 * delta_time * 100))

    lightning._parameter += 1 * delta_time * 100

    if lightning._parameter > 500:
        lightnings.remove(lightning)
        del lightning

def create_candy_cane() -> None:
    global candy_canes

    candy_cane: GameObject = GameObject()
    candy_cane.set_image("Images/CandyCane.png")
    candy_cane.set_position((1450 + 100, -800))
    candy_cane.set_rotation(90)
    candy_canes.append(candy_cane)

candy_cane_rot_delay: float = 0
def update_candy_cane(candy_cane: GameObject, delta_time: float) -> None:
    global candy_cane_rot_delay, candy_canes

    candy_cane.set_position((candy_cane._position[0] - 10 * delta_time * 100, candy_cane._position[1]))

    if candy_cane._position[0] < -100:
        candy_canes.remove(candy_cane)
        del candy_cane


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

def create_bullet(bullet_position: tuple[int, int], bullet_direction: tuple[int, int], current_player_weapon: str) -> None:
    if current_player_weapon == "pistol":
        bullet: Bullet = Bullet(current_level_targets)
        bullet.set_direction(bullet_direction)
        bullet.set_position(bullet_position)
        current_level_bullets.append(bullet)
    elif current_player_weapon == "shotgun":
        middle_bullet: Bullet = Bullet(current_level_targets)
        middle_bullet.set_direction(bullet_direction)
        middle_bullet.set_position(bullet_position)
        middle_bullet.set_duration(25)
        middle_bullet._image = pygame.image.load("Images/RedBullet.png")
        current_level_bullets.append(middle_bullet)

        if not bullet_direction[0] == 0:
            rotation_multi: int = 1
            if bullet_direction[0] < 0:
                rotation_multi = -1

            top_bullet: Bullet = Bullet(current_level_targets)
            top_bullet.set_direction((bullet_direction[0], 0.5))
            top_bullet.set_position(bullet_position)
            top_bullet.set_duration(25)
            top_bullet._image = pygame.image.load("Images/RedBullet.png")
            top_bullet._image = pygame.transform.rotate(top_bullet._image, 22.5 * rotation_multi)
            top_bullet._rect = top_bullet._image.get_rect()
            
            bottom_bullet: Bullet = Bullet(current_level_targets)
            bottom_bullet.set_direction((bullet_direction[0], -0.5))
            bottom_bullet.set_position(bullet_position)
            bottom_bullet.set_duration(25)
            bottom_bullet._image = pygame.image.load("Images/RedBullet.png")
            bottom_bullet._image = pygame.transform.rotate(bottom_bullet._image, -22.5 * rotation_multi)
            bottom_bullet._rect = bottom_bullet._image.get_rect()

            current_level_bullets.append(top_bullet)
            current_level_bullets.append(bottom_bullet)
        else:
            top_bullet: Bullet = Bullet(current_level_targets)
            top_bullet.set_direction((0.5, bullet_direction[1]))
            top_bullet.set_position(bullet_position)
            top_bullet.set_duration(25)
            top_bullet._image = pygame.image.load("Images/RedBullet.png")
            top_bullet._image = pygame.transform.rotate(top_bullet._image, 45)
            top_bullet._rect = top_bullet._image.get_rect()
            
            bottom_bullet: Bullet = Bullet(current_level_targets)
            bottom_bullet.set_direction((-0.5, bullet_direction[1]))
            bottom_bullet.set_position(bullet_position)
            bottom_bullet.set_duration(25)
            bottom_bullet._image = pygame.image.load("Images/RedBullet.png")
            bottom_bullet._image = pygame.transform.rotate(bottom_bullet._image, -45)
            bottom_bullet._rect = bottom_bullet._image.get_rect()

            current_level_bullets.append(top_bullet)
            current_level_bullets.append(bottom_bullet)

            middle_bullet._image = pygame.transform.rotate(middle_bullet._image, -90)
            middle_bullet._rect = middle_bullet._image.get_rect()

def remove_bullet(bullet: Bullet) -> None:
    if bullet in current_level_bullets:
        current_level_bullets.remove(bullet)
    
    del bullet

def render_level(level: str, screen: pygame.display, delta_time: float) -> None:
    global plr, current_level_game_objects, current_level_bullets, background_game_object, ground_game_object, boss, tracked_carrots, carrot_track_delay, cloud, lightnings, candy_canes

    background_game_object.render(screen)

    for game_object in current_level_game_objects:
        game_object.render(screen)

    boss.update(delta_time)
    boss.render(screen)

    for tracked_carrot in tracked_carrots:
        tracked_carrot.render(screen)

        track_carrot(tracked_carrot, delta_time, carrot_track_delay)
    
    if carrot_track_delay > 0:
        carrot_track_delay -= 1 * delta_time * 100
    else:
        carrot_track_delay = 150

    if cloud:
        cloud.render(screen)
        handle_cloud(delta_time)
    
    for lightning in lightnings:
        lightning.render(screen)
        update_lightning(lightning, delta_time)
    
    for candy_cane in candy_canes:
        candy_cane.render(screen)
        update_candy_cane(candy_cane, delta_time)

    if plr._position[1] < -900:
        plr.set_position([0, 0])
    
    if plr._position[0] < 0:
        plr.set_position([0, plr._position[1]])
        plr._dash = 0
    elif plr._position[0] > 1840 - 70:
        plr.set_position([1840 - 70, plr._position[1]])
        plr._dash = 0

    for bullet in current_level_bullets:
        bullet.update(delta_time)
        bullet.render(screen)

    plr.ground_check(current_level_game_objects, delta_time)
    plr.update(delta_time)
    plr.render(screen, delta_time)

    ParticleEmitter.handle_particle_emmitters(screen)

    ground_game_object.render(screen)

