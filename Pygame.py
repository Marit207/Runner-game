import pygame
from sys import exit
import math
from random import randint, choice

class Player(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    player_walk_1 = pygame.image.load('character_robot_run0.png').convert_alpha()
    player_walk_2 = pygame.image.load('character_robot_run1.png').convert_alpha()
    player_walk_3 = pygame.image.load('character_robot_run2.png').convert_alpha()
    self.player_walk = [player_walk_1, player_walk_2, player_walk_3]
    self.player_index = 0
    self.player_jump = pygame.image.load('character_robot_jump.png').convert_alpha()
    
    self.image = self.player_walk[self.player_index]
    self.rect = self.image.get_rect(midbottom = (50,445))
    self.gravity = 0

    self.jump_sound = pygame.mixer.Sound('jump.mp3')
    self.jump_sound.set_volume(0.5)

  def player_input(self):
    keys = pygame.key.get_pressed()
    if game_active:
      if keys[pygame.K_SPACE] and self.rect.bottom >= 345:
        self.gravity = -15
        self.jump_sound.play()
        
  def apply_gravity(self):
    self.gravity += 0.6
    self.rect.y += self.gravity
    if self.rect.bottom >= 350:
      self.rect.bottom = 350
  
  def animation_state(self):
    if self.rect.bottom < 345:
      self.image = self.player_jump
    else:
      self.player_index += 0.1
      if self.player_index >= len(self.player_walk):
         self.player_index = 0
      self.image = self.player_walk[int(self.player_index)]

  def update(self):
    self.player_input()
    self.apply_gravity()
    self.animation_state()

class Obstacle(pygame.sprite.Sprite):
  def __init__(self,type):
    super().__init__()

    if type == 'fly':
      fly_frame_1 = pygame.image.load('bee.png').convert_alpha()
      fly_frame_2 = pygame.image.load('bee_fly.png').convert_alpha()
      self.frames = [fly_frame_1, fly_frame_2]
      y_pos = 210
    else:
      snail_frame_1 = pygame.image.load('snail.png').convert_alpha()
      snail_frame_2 = pygame.image.load('snail_walk.png').convert_alpha()
      self.frames = [snail_frame_1, snail_frame_2]
      y_pos = 350

    self.animation_index = 0
    self.image = self.frames[self.animation_index]
    self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

  def animation_state(self):
    self.animation_index += 0.1
    if self.animation_index >= len(self.frames):
      self.animation_index = 0
    self.image = self.frames[int(self.animation_index)]
  
  def destroy(self):
    if self.rect.x <= -100:
      self.kill()

  def update(self):
    self.animation_state()
    self.rect.x -= 6
    self.destroy()


def display_score():
  current_time = int(pygame.time.get_ticks() / 1000) - start_time
  font = pygame.font.Font(None, 36)
  score_surf = font.render(f'Score: {current_time}', False, (64, 64, 64))
  score_rect = score_surf.get_rect(center = (400,50))
  screen.blit(score_surf, score_rect)
  return current_time

def collision_sprite():
  if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
    obstacle_group.empty()
    return False
  else:
    return True

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Pygame")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('Fluffing-a-Duck.mp3')
bg_music.set_volume(0.5)
bg_music.play(loops=-1)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# Background
surface_brown = pygame.image.load('47784.jpg').convert_alpha()
background = pygame.transform.scale(surface_brown, (600,400))
bg_width = background.get_width()

scroll = 0
tiles = math.ceil(800 / bg_width) + 1

player_walk_1 = pygame.image.load('character_robot_run0.png').convert_alpha()

# intro screen
player_stand = pygame.image.load('character_robot_run0.png').convert_alpha()
player_stand_rect = player_walk_1.get_rect(center = (400,200))

game_title_surf = font.render("Pixel runner", False, (0, 0, 100))
game_title_rect = game_title_surf.get_rect(center = (400, 50))

start_instr = font.render("Press space to start", False, (0, 0, 100))
start_instr_rect = start_instr.get_rect(center = (400, 350))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1400)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()
        
    if game_active: 
        if event.type == obstacle_timer:
          obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))

    else:
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        game_active = True
        start_time = int(pygame.time.get_ticks() / 1000)

  if game_active:         
    score = display_score()
    scroll -= 3
    for i in range(0, tiles):
      screen.blit(background, (i * bg_width + scroll, 0))

    if abs(scroll) > bg_width:
      scroll = 0

    player.draw(screen)
    player.update()

    obstacle_group.draw(screen)
    obstacle_group.update()
    
    # Collision
    game_active = collision_sprite()
  
  else:
      screen.fill((0, 200, 255))
      screen.blit(player_stand, player_stand_rect)
      screen.blit(game_title_surf, game_title_rect)
     
      score_surf = font.render(f"Score: {score}", False, (0, 0, 100))
      score_surf_rect = score_surf.get_rect(center = (400, 350))
      
      if score == 0:
        screen.blit(start_instr, start_instr_rect)
      else:
        screen.blit(score_surf, score_surf_rect)
   
  pygame.display.update()
  clock.tick(60)