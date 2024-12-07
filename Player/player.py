from __future__ import annotations
import pygame
from GameObjects.game_object import GameObject, ParticleEmitter
import Level.level_handler

image_load: pygame.image.load = pygame.image.load

class Player:
    def __init__(self) -> None:
        self._position = [0, 0]
        self._image = image_load("Images/PlayerIdleLeft.png")
        self._rect = self._image.get_rect()
        self._movespeed = 400
        self._horizontal = 0
        self._vertical = 0
        self._gravity = 9.81
        self._grounded = False
        self._horizontal_collision = "none"
        self._idle_left_images = [image_load("Images/PlayerIdleLeft.png"), image_load("Images/PlayerIdleLeft_1.png")]
        self._idle_right_images = [image_load("Images/PlayerIdleRight.png"), image_load("Images/PlayerIdleRight_1.png")]
        self._walk_left_images = [image_load("Images/PlayerWalkLeft_1.png"), image_load("Images/PlayerIdleLeft.png"), image_load("Images/PlayerWalkLeft_1.png"), image_load("Images/PlayerIdleLeft.png")]
        self._walk_right_images = [image_load("Images/PlayerWalkRight_1.png"), image_load("Images/PlayerIdleRight.png"), image_load("Images/PlayerWalkRight_1.png"), image_load("Images/PlayerIdleRight.png")]
        self._jump_left = image_load("Images/PlayerJumpLeft.png")
        self._jump_right = image_load("Images/PlayerJumpRight.png")
        self._crouch_idle_left = []
        self._crouch_idle_right = []
        self._crouch_walk_left = []
        self._crouch_walk_right = []
        self._walk_animation_frame = 0
        self._idle_animation_frame = 0
        self._last_side = 1
        self._ground_delay = 0
        self._crouch = False
        self._crouch_height_diff = 2
        self._main_ground = False
        self._skip_grounded = 0
        self._dash = 0
        self._dash_direction = 0
        self._dash_cooldown = 0
        self._dash_images = [image_load("Images/PlayerDashLeft.png"), image_load("Images/PlayerDashRight.png")]
        self._dash_air_block = False
        self._bullet_delay = 0
        self._bullet_delay_up = 0
        self._shoot_images = [image_load("Images/PlayerShootLeft.png"), image_load("Images/PlayerShootRight.png")]
        self._shoot_walk_left_images = [image_load("Images/PlayerWalkLeft_1_gun.png"), image_load("Images/PlayerShootLeft.png"), image_load("Images/PlayerWalkLeft_1_gun.png"), image_load("Images/PlayerShootLeft.png")]
        self._shoot_walk_right_images = [image_load("Images/PlayerWalkRight_1_gun.png"), image_load("Images/PlayerShootRight.png"), image_load("Images/PlayerWalkRight_1_gun.png"), image_load("Images/PlayerShootRight.png")]
        self._shoot_jump_images = [image_load("Images/PlayerJumpLeft_gun.png"), image_load("Images/PlayerJumpRight_gun.png")]
        self._shoot_up_images = [image_load("Images/PlayerShootUpLeft.png"), image_load("Images/PlayerShootUpRight.png")]
        self._shoot_up_jump_images = [image_load("Images/PlayerJumpLeft_shoot.png"), image_load("Images/PlayerJumpRight_shoot.png")]
        self._crouch_shoot_images = []
        self._crouch_shoot_walk_left_images = []
        self._crouch_shoot_walk_right_images = []
        self._crouch_shoot_up_images = []
        self._jump_particles = ParticleEmitter()
        self._dash_particles = ParticleEmitter()
        self._walk_particle_delay = 0
        self._current_weapon = "pistol"
        self._weapon_delay = 0

        self.load_crouch_animations()
        self.set_particle_emitters()
    
    def set_particle_emitters(self) -> None:
        self._jump_particles.set_particle_image("Images/SnowParticle.png")
        self._jump_particles.set_emitter(1000, (0, 0), (0, 0), [(5, 5), (-5, 5), (0, 5)], 20, 5, False, (-5, 5, 3, 7))

        self._dash_particles.set_particle_image("Images/SnowParticle.png")
        self._dash_particles.set_emitter(1000, (0, 0), (0, 0), [(0, 0)], 20, 5, False, (-5, 5, -5, 5))

    def load_crouch_animations(self) -> None:
        for anim_frame in self._idle_left_images:
            self._crouch_idle_left.append(pygame.transform.scale(anim_frame, [self._rect.width, self._rect.height / self._crouch_height_diff]))

        for anim_frame in self._idle_right_images:
            self._crouch_idle_right.append(pygame.transform.scale(anim_frame, [self._rect.width, self._rect.height / self._crouch_height_diff]))
        
        for anim_frame in self._walk_left_images:
            self._crouch_walk_left.append(pygame.transform.scale(anim_frame, [self._rect.width, self._rect.height / self._crouch_height_diff]))

        for anim_frame in self._walk_right_images:
            self._crouch_walk_right.append(pygame.transform.scale(anim_frame, [self._rect.width, self._rect.height / self._crouch_height_diff]))
        
        for anim_frame in self._shoot_images:
            self._crouch_shoot_images.append(pygame.transform.scale(anim_frame, [self._rect.width, self._rect.height / self._crouch_height_diff]))
        
        for anim_frame in self._shoot_walk_left_images:
            self._crouch_shoot_walk_left_images.append(pygame.transform.scale(anim_frame, [self._rect.width, self._rect.height / self._crouch_height_diff]))
        
        for anim_frame in self._shoot_walk_right_images:
            self._crouch_shoot_walk_right_images.append(pygame.transform.scale(anim_frame, [self._rect.width, self._rect.height / self._crouch_height_diff]))
        
        self._crouch_shoot_up_images.append(pygame.transform.scale(self._shoot_up_images[0], [self._rect.width, self._rect.height / self._crouch_height_diff]))
        self._crouch_shoot_up_images.append(pygame.transform.scale(self._shoot_up_images[1], [self._rect.width, self._rect.height / self._crouch_height_diff]))

    def set_position(self, position: tuple[int, int]) -> None:
        self._position = position
    
    def animate(self, delta_time) -> None:
        if self._idle_animation_frame +1 >= 40:
            self._idle_animation_frame = 0
        
        if self._walk_animation_frame +1 >= 80:
            self._walk_animation_frame = 0
        
        if self._dash > 0:
            if self._dash_direction > 0:
                self._image = self._dash_images[0]
            else:
                self._image = self._dash_images[1]
        elif self._bullet_delay_up > 0:
            if self._vertical > 0 and not self._crouch or self._vertical < 0 and self._ground_delay > 5 and not self._crouch:
                if self._last_side > 0:
                    self._image = self._shoot_up_jump_images[0]
                else:
                    self._image = self._shoot_up_jump_images[1]
            else:
                if self._last_side > 0:
                    if self._crouch:
                        self._image = self._crouch_shoot_up_images[0]
                    else:
                        self._image = self._shoot_up_images[0]
                else:
                    if self._crouch:
                        self._image = self._crouch_shoot_up_images[1]
                    else:
                        self._image = self._shoot_up_images[1]
        else:
            if self._vertical > 0 and not self._crouch or self._vertical < 0 and self._ground_delay > 5 and not self._crouch:
                if self._last_side == 0 or self._last_side > 0:
                    if self._bullet_delay > 0:
                        self._image = self._shoot_jump_images[0]
                    else:
                        self._image = self._jump_left
                else:
                    if self._bullet_delay > 0:
                        self._image = self._shoot_jump_images[1]
                    else:
                        self._image = self._jump_right
            else:
                if not self._horizontal == 0:
                    if self._horizontal > 0:
                        if self._crouch:
                            if self._bullet_delay > 0:
                                self._image = self._crouch_shoot_walk_left_images[self._walk_animation_frame // 20]
                            else:
                                self._image = self._crouch_walk_left[self._walk_animation_frame // 20]
                        elif self._bullet_delay > 0:
                            self._image = self._shoot_walk_left_images[self._walk_animation_frame // 20]
                        else:
                            self._image = self._walk_left_images[self._walk_animation_frame // 20]
                        self._walk_animation_frame += 1 * int(delta_time * 100)
                    else:
                        if self._crouch:
                            if self._bullet_delay > 0:
                                self._image = self._crouch_shoot_walk_right_images[self._walk_animation_frame // 20]
                            else:
                                self._image = self._crouch_walk_right[self._walk_animation_frame // 20]
                        elif self._bullet_delay > 0:
                            self._image = self._shoot_walk_right_images[self._walk_animation_frame // 20]
                        else:
                            self._image = self._walk_right_images[self._walk_animation_frame // 20]
                        self._walk_animation_frame += 1 * int(delta_time * 100)
                else:
                    if self._last_side == 0 or self._last_side > 0:
                        if self._crouch:
                            if self._bullet_delay > 0:
                                self._image = self._crouch_shoot_images[0]
                            else:
                                self._image = self._crouch_idle_left[self._idle_animation_frame // 20]
                        elif self._bullet_delay > 0:
                            self._image = self._shoot_images[0]
                        else:
                            self._image = self._idle_left_images[self._idle_animation_frame // 20]
                    else:
                        if self._crouch:
                            if self._bullet_delay > 0:
                                self._image = self._crouch_shoot_images[1]
                            else:
                                self._image = self._crouch_idle_right[self._idle_animation_frame // 20]
                        elif self._bullet_delay > 0:
                            self._image = self._shoot_images[1]
                        else:
                            self._image = self._idle_right_images[self._idle_animation_frame // 20]
            
                    self._idle_animation_frame += 1 * int(delta_time * 100)

    def ground_check(self, game_objects: list[GameObject], delta_time: float) -> None:
        grounded: bool = False
        horizontal_collision: str = "none"

        for game_object in game_objects:
            if self._rect.colliderect(game_object._rect) and self._rect.bottom <= game_object._rect.top + self._vertical * delta_time * 10 *-1:
                if self._skip_grounded <= 0 or game_object._tag == "ground":
                    self._position = [self._position[0], game_object._position[1] + self._rect.height - 1]
                    grounded = True

                if game_object._tag == "ground":
                    self._main_ground = True
                else:
                    self._main_ground = False

            #if self._rect.colliderect(game_object._rect) and self._rect.bottom > game_object._rect.bottom:
                #if self._horizontal > 0:
                    #horizontal_collision = "right"
                    #self._position = [game_object._rect.left - self._rect.width, self._position[1]]
                    #pass
                #elif self._horizontal < 0:
                    #horizontal_collision = "left"
                    #self._position = [game_object._rect.right, self._position[1]]
                    #pass

        self._grounded = grounded
        self._horizontal_collision = horizontal_collision

    def crouch(self, delta_time: float) -> None:
        if self._crouch:
            self._rect = self._crouch_idle_left[0].get_rect()
            self._position = [self._position[0], self._position[1] - self._rect.height/1.05]
        else:
            self._rect = self._idle_left_images[0].get_rect()
            self._position = [self._position[0], self._position[1] + self._rect.height/1.05/1.95]

    def update(self, delta_time: float) -> None:
        key: pygame.key = pygame.key.get_pressed()

        if key[pygame.K_d] and not key[pygame.K_a]:
            self._horizontal = 1
            self._last_side = 1
        elif key[pygame.K_a] and not key[pygame.K_d]:
            self._horizontal = -1
            self._last_side = -1
        else:
            self._horizontal = 0

        if not self._grounded:
            if self._dash <= 5:
                self._vertical -= self._gravity * 2 * 1.5 * delta_time * 100 * 2
            self._ground_delay += 1 * delta_time * 100
        else:
            if self._ground_delay > 10:
                self._jump_particles.emit(5, (int(self._position[0] + self._rect.width/2), int(self._position[0] + self._rect.width/2)), 
                                          (int(self._position[1] - self._rect.height), int(self._position[1] - self._rect.height)))

            self._vertical = 0
            self._ground_delay = 0
            self._dash_air_block = False
        
        if key[pygame.K_s] and self._ground_delay < 20 and self._dash <= 0:
            if not self._crouch:
                self._crouch = True
                self.crouch(delta_time)
        else:
            if self._crouch:
                self._crouch = False
                self.crouch(delta_time)
        
        if key[pygame.K_SPACE] and self._grounded:
            if not self._crouch:
                self._vertical = 1000 * 1.35 * 1.25
                self._jump_particles.emit(5, (int(self._position[0] + self._rect.width/2), int(self._position[0] + self._rect.width/2)), 
                                          (int(self._position[1] - self._rect.height), int(self._position[1] - self._rect.height)))
            elif not self._main_ground:
                self._skip_grounded = 50
                self._grounded = False
                self._crouch = False
                self.crouch(delta_time)
        
        if key[pygame.K_LSHIFT] and self._dash <= 0 and self._dash_cooldown <= 0 and not self._dash_air_block:
            self._dash = 30
            self._dash_direction = self._last_side

            if self._crouch:
                self._crouch = False
                self.crouch(delta_time)
            
            if not self._grounded:
                self._dash_air_block = True
            
            self._dash_particles.emit(10, (int(self._position[0] + self._rect.width/2), int(self._position[0] + self._rect.width/2)),
                                      (int(self._position[1] - self._rect.height/2), int(self._position[1] - self._rect.height/2)))
        
        if key[pygame.K_1] and self._weapon_delay <= 0:
            if self._current_weapon == "pistol":
                self._current_weapon = "shotgun"
            else:
                self._current_weapon = "pistol"
            
            self._weapon_delay = 30

        if key[pygame.K_f] and self._bullet_delay <= 1 and self._dash <= 0:
            fix: int = 20

            if self._crouch:
                fix = 0
            
            bullet_position: tuple[int, int]
            bullet_direction: tuple[int, int]

            if key[pygame.K_w] and self._horizontal == 0:
                if self._last_side > 0:
                    bullet_position = [self._position[0] + self._rect.width/2 + 35, self._position[1]]
                else:
                    bullet_position = [self._position[0] + self._rect.width/2 - 60, self._position[1]]                    

                bullet_direction = [0, 1]
                self._bullet_delay_up = 35
            else:
                bullet_position = [(self._position[0] + self._rect.width/2) + self._rect.width/2 * self._last_side, self._position[1] - self._rect.height/2 - fix]
                bullet_direction = [self._last_side, 0]

            Level.level_handler.create_bullet(bullet_position, bullet_direction, self._current_weapon)

            self._bullet_delay = 35
        
        if self._weapon_delay > 0:
            self._weapon_delay -= 1

        if self._bullet_delay > 0:
            self._bullet_delay -= 1 * delta_time * 200
        
        if self._bullet_delay_up > 0:
            self._bullet_delay_up -= 1
        
        if self._skip_grounded > 0:
            self._skip_grounded -= 1

        if self._dash_cooldown > 0:
            self._dash_cooldown -= 1

        if not self._horizontal == 0 and self._ground_delay < 10:
            if self._walk_particle_delay < 10:
                self._walk_particle_delay += 1
            else:
                self._walk_particle_delay = 0
                self._jump_particles.emit(1, (int(self._position[0] + self._rect.width/2), int(self._position[0] + self._rect.width/2)), 
                                        (int(self._position[1] - self._rect.height), int(self._position[1] - self._rect.height)))
        else:
            self._walk_particle_delay = 0

        if self._dash <= 0:
            self._position = [self._position[0] + self._movespeed * delta_time * self._horizontal, self._position[1] + self._vertical * delta_time]
        else:
            self._position = [self._position[0] + 300 * 5 * delta_time * self._dash_direction, self._position[1]]
            self._dash -= 1 * delta_time * 100
            self._dash_cooldown = 50

    def render(self, screen: pygame.display, delta_time: float) -> None:
        self.animate(delta_time)

        self._rect.topleft = (self._position[0], -self._position[1])

        screen.blit(self._image, self._rect)