from __future__ import annotations
import pygame
import Level.level_handler
import random

image_load: pygame.image.load = pygame.image.load

class GameObject:
    def __init__(self) -> None:
        self._position = [0, 0]
        self._image = image_load("Images/Platform.png")
        self._rect = self._image.get_rect()
        self._tag = ""
        self._direction = [0, 0]
        self._velocity = [0, 0]
        self._parameter = 0
        self._rotation = 0
    
    def set_position(self, position: tuple[int, int]) -> None:
        self._position = position
    
    def set_rotation(self, rotation: float) -> None:
        self._rotation = rotation
        self._image = pygame.transform.rotate(self._image, rotation)
        self._rect = self._image.get_rect()
    
    def set_image(self, image: str) -> None:
        self._image = pygame.image.load(image)
        self._rect = self._image.get_rect()
    
    def render(self, screen: pygame.display) -> None:
        self._rect.topleft = (self._position[0], -self._position[1])

        screen.blit(self._image, self._rect)

class Particle(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], image: str) -> None:
        super().__init__()
        self._position = position
        self.image = image_load(image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self._duration = 0
        self._velocity = [0, 0]
    
    def set_position(self, position: tuple[int, int]) -> None:
        self._position = position
        self.rect.topleft = (self._position[0], self._position[1])

    def set_velocity(self, velocity: tuple[int, int]) -> None:
        self._velocity = velocity
    
    def render(self, screen: pygame.display) -> None:
        self.rect.topleft = (self._position[0], -self._position[1])

        screen.blit(self.image, self.rect)

class ParticleEmitter:
    particle_emitters: list[ParticleEmitter] = []

    def __init__(self) -> None:
        self._particles = []
        self._particle_group = pygame.sprite.Group()
        self._spawn_delay = 120
        self._spawn_x = (0, 1000)
        self._spawn_y = (0, 100)
        self._velocity = [(0, 0)]
        self._velocity_range = (0, 0, 0, 0)
        self._duration = 120
        self._emit_count = 10
        self._particle_image = "Images/SnowParticle.png"
        self._auto_emit = True

        self.__cur = 0
        self.__use_vel_range = False
        ParticleEmitter.particle_emitters.append(self)

    def set_emitter(self, spawn_delay: int, spawn_range_x: tuple[int, int], spawn_range_y: tuple[int, int], particle_velocity: list[tuple[int, int]], particle_duration: int,
                    emit_count: int, auto_emit: bool = True, velocity_range: tuple[int, int, int, int] = (0, 0, 0, 0)) -> None:
        self._spawn_delay = spawn_delay
        self._spawn_x = spawn_range_x
        self._spawn_y = spawn_range_y
        self._velocity = particle_velocity
        self._duration = particle_duration
        self._emit_count = emit_count
        self._auto_emit = auto_emit
        self._velocity_range = velocity_range

        if not velocity_range == (0, 0, 0, 0):
            self.__use_vel_range = True
        else:
            self.__use_vel_range = False
    
    def set_particle_image(self, image: str) -> None:
        self._particle_image = image

    def create_particle(self, spawn_x: tuple[int, int], spawn_y: tuple[int, int]) -> None:
        particle: Particle = Particle([random.randint(spawn_x[0], spawn_x[1]), random.randint(spawn_y[0], spawn_y[1])], self._particle_image)

        if self.__use_vel_range:
            velocity: tuple[int, int] = (random.randint(self._velocity_range[0], self._velocity_range[1]), random.randint(self._velocity_range[2], self._velocity_range[3]))
        else:
            velocity: tuple[int, int] = self._velocity[random.randint(0, len(self._velocity) - 1)]

        particle.set_velocity(velocity)
        self._particles.append(particle)
        #self._particle_group.add(particle)

    def emit(self, particle_count: int, spawn_x: tuple[int, int], spawn_y: tuple[int, int]) -> None:
        for _ in range(particle_count):
            self.create_particle(spawn_x, spawn_y)

    def render(self, screen: pygame.display) -> None:
        self.__cur += 1
        if self.__cur >= self._spawn_delay:
            self.__cur = 0
            if self._auto_emit:
                self.emit(self._emit_count, self._spawn_x, self._spawn_y)

        particles_to_remove: list[Particle] = []

        for particle in self._particles:
            particle.set_position([particle._position[0] + particle._velocity[0], particle._position[1] + particle._velocity[1]])
            particle._duration += 1

            particle.render(screen)

            if particle._duration >= self._duration:
                particles_to_remove.append(particle)
        
        #self._particle_group.draw(screen)
        
        for particle_to_remove in particles_to_remove:
            self._particles.remove(particle_to_remove)
        
        while particles_to_remove:
            del particles_to_remove[0]

    @classmethod
    def handle_particle_emmitters(cls, screen: pygame.display) -> None:
        for particle_emitter in cls.particle_emitters:
            particle_emitter.render(screen)     

class Bullet:
    def __init__(self, targets: list) -> None:
        self._position = [0, 0]
        self._image = image_load("Images/Bullet.png")
        self._rect = self._image.get_rect()
        self._damage = 1
        self._speed = 1500
        self._direction = [0, 0]
        self._duration = -1
        self._targets = targets
    
    def set_targets(self, targets: list) -> None:
        self._targets = targets

    def set_position(self, position: tuple[int, int]) -> None:
        self._position = position
    
    def set_direction(self, direction: tuple[int, int]) -> None:
        self._direction = direction

        if self._direction == [0, 1]:
            self._image = pygame.transform.rotate(self._image, 90)
            self._rect = self._image.get_rect()

    def set_duration(self, duration: int) -> None:
        self._duration = duration

    def update(self, delta_time: float) -> None:
        self._position = [self._position[0] + self._speed * delta_time * self._direction[0], self._position[1] + self._speed * delta_time * self._direction[1]]

        for target in self._targets:
            if self._rect.colliderect(target._rect):
                if type(target) == Boss:
                    target.take_damage(self._damage)
                else:
                    target._parameter -= 1
                    if target._parameter <= 0:
                        Level.level_handler.remove_tracked_carrot(target)

                Level.level_handler.remove_bullet(self)

        if not self._duration == -1:
            self._duration -= 1
            if self._duration <= 0:
                Level.level_handler.remove_bullet(self)

    def render(self, screen: pygame.display) -> None:
        self._rect.topleft = (self._position[0], -self._position[1])

        screen.blit(self._image, self._rect)

        if self._position[0] < -2000 or self._position[0] > 2000 or self._position[1] > 2000 or self._position[1] < -2000:
            Level.level_handler.remove_bullet(self)

class Boss:
    def __init__(self, health: float) -> None:
        self._health = health
        self._idle_images = [image_load("Images/BossDefault.png"), image_load("Images/BossDefault2.png")]
        self._attack1 = image_load("Images/Attack1.png")
        self._attack2 = image_load("Images/Attack2.png")
        self._state = "idle"
        self._image = image_load("Images/BossDefault.png")
        self._rect = self._image.get_rect()
        self._position = (0, 0)
        self._idle_animation_frame = 0
        self._phase_counter = 0
        self._phase = 0
        self._carrot_anim_counter = 0
        self._cloud_anim_counter = 0
        self._candy_cane_anim_counter = 0

    def set_position(self, position: tuple[int, int]) -> None:
        self._position = position

    def take_damage(self, damage: float) -> None:
        self._health -= damage

        if self._health <= 0:
            Level.level_handler.victory()

    def animate(self) -> None:
        if self._idle_animation_frame +1 >= 40:
            self._idle_animation_frame = 0
        
        if self._carrot_anim_counter > 0:
            self._image = self._attack1
            self._position = (self._position[0], 50)
        elif self._cloud_anim_counter > 0:
            self._image = self._attack2
        elif self._candy_cane_anim_counter > 0: 
            self._position = (self._position[0], -150)
        else:
            self._image = self._idle_images[self._idle_animation_frame // 20]
            self._rect = self._image.get_rect()
            self._idle_animation_frame += 1
            self._position = (self._position[0], -350)
    
    def tracked_carrot(self) -> None:
        self._carrot_anim_counter = 60
        self._rect = self._attack1.get_rect()

        Level.level_handler.create_tracked_carrot()
        Level.level_handler.create_tracked_carrot()
        Level.level_handler.create_tracked_carrot()
    
    def cloud(self) -> None:
        self._cloud_anim_counter = 35

        Level.level_handler.create_cloud()
    
    def candy_cane(self, version: int) -> None:
        if version == 0:
            self._candy_cane_anim_counter = 60
        else:
            self._carrot_anim_counter = 60

        Level.level_handler.create_candy_cane(version)

    def handle_phases(self, delta_time: float) -> None:
        if self._phase == 0:
            self._phase_counter += 1 * delta_time * 100

            if self._phase_counter > 450:
                self._phase_counter = 0

                event: int = random.randint(0, 3)

                match event:
                    case 1:
                        self.cloud()
                    case 2:
                        self.candy_cane(0)
                    case 3:
                        self.candy_cane(1)
                    case _:
                        self.tracked_carrot()

    def update(self, delta_time: float) -> None:
        self.animate()
        self.handle_phases(delta_time)

        if self._carrot_anim_counter > 0:
            self._carrot_anim_counter -= 1 * delta_time * 100
        
        if self._cloud_anim_counter > 0:
            self._cloud_anim_counter -= 1 * delta_time * 100

        if self._candy_cane_anim_counter > 0:
            self._candy_cane_anim_counter -= 1 * delta_time * 100

    def render(self, screen: pygame.display) -> None:
        self._rect.topleft = (self._position[0], -self._position[1])

        screen.blit(self._image, self._rect)