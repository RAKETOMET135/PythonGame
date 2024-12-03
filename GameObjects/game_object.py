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
    
    def set_position(self, position: tuple[int, int]) -> None:
        self._position = position
    
    def set_image(self, image: str) -> None:
        self._image = pygame.image.load(image)
        self._rect = self._image.get_rect()
    
    def render(self, screen: pygame.display) -> None:
        self._rect.topleft = (self._position[0], -self._position[1])

        screen.blit(self._image, self._rect)

class Particle:
    def __init__(self, position: tuple[int, int], image: str) -> None:
        self._position = position
        self._image = image_load(image)
        self._rect = self._image.get_rect()
        self._duration = 0
    
    def set_position(self, position: tuple[int, int]) -> None:
        self._position = position
    
    def render(self, screen: pygame.display) -> None:
        self._rect.topleft = (self._position[0], -self._position[1])

        screen.blit(self._image, self._rect)

class ParticleEmitter:
    particle_emitters: list[ParticleEmitter] = []

    def __init__(self) -> None:
        self._particles = []
        self._spawn_delay = 120
        self._spawn_x = [0, 1000]
        self._spawn_y = [0, 100]
        self._velocity = [0, 0]
        self._duration = 120
        self._emit_count = 10

        self.__cur = 0
        ParticleEmitter.particle_emitters.append(self)

    def set_emitter(self, spawn_delay: int, spawn_range_x: tuple[int, int], spawn_range_y: tuple[int, int], particle_velocity: tuple[int, int], particle_duration: int,
                    emit_count: int) -> None:
        self._spawn_delay = spawn_delay
        self._spawn_x = spawn_range_x
        self._spawn_y = spawn_range_y
        self._velocity = particle_velocity
        self._duration = particle_duration
        self._emit_count = emit_count

    def create_particle(self) -> None:
        particle: Particle = Particle([random.randint(self._spawn_x[0], self._spawn_x[1]), random.randint(self._spawn_y[0], self._spawn_y[1])], "Images/SnowParticle.png")
        self._particles.append(particle)

    def emit(self, particle_count: int) -> None:
        for _ in range(particle_count):
            self.create_particle()

    def render(self, screen: pygame.display) -> None:
        self.__cur += 1
        if self.__cur >= self._spawn_delay:
            self.__cur = 0
            self.emit(self._emit_count)

        particles_to_remove: list[Particle] = []

        for particle in self._particles:
            particle.set_position([particle._position[0] + self._velocity[0], particle._position[1] + self._velocity[1]])
            particle._duration += 1

            particle.render(screen)

            if particle._duration >= self._duration:
                particles_to_remove.append(particle)
        
        for particle_to_remove in particles_to_remove:
            self._particles.remove(particle_to_remove)
            del particles_to_remove

    @classmethod
    def handle_particle_emmitters(cls, screen: pygame.display) -> None:
        for particle_emitter in cls.particle_emitters:
            particle_emitter.render(screen)     

class Bullet:
    def __init__(self) -> None:
        self._position = [0, 0]
        self._image = image_load("Images/Bullet.png")
        self._rect = self._image.get_rect()
        self._damage = 1
        self._speed = 1500
        self._direction = [0, 0]
    
    def set_position(self, position: tuple[int, int]) -> None:
        self._position = position
    
    def set_direction(self, direction: tuple[int, int]) -> None:
        self._direction = direction

        if self._direction == [0, 1]:
            self._image = pygame.transform.rotate(self._image, 90)
            self._rect = self._image.get_rect()

    def update(self, delta_time: float) -> None:
        self._position = [self._position[0] + self._speed * delta_time * self._direction[0], self._position[1] + self._speed * delta_time * self._direction[1]]

    def render(self, screen: pygame.display) -> None:
        self._rect.topleft = (self._position[0], -self._position[1])

        screen.blit(self._image, self._rect)

        if self._position[0] < -2000 or self._position[0] > 2000 or self._position[1] > 2000 or self._position[1] < -2000:
            Level.level_handler.remove_bullet(self)
