from typing import Any
import pygame
from random import randint, choice
import asyncio


import os, sys 

def chdir(): # for „change directory“
        absolute_path = os.path.abspath(sys.argv[0])
        directory_name = os.path.dirname(absolute_path)
        os.chdir(directory_name)

class Ghost(pygame.sprite.Sprite):
    def __init__(self,):
        super().__init__()
        
        ghost_1 = pygame.image.load('/Users/chirathrashmika/Desktop/Pixel_ghost/graphics/ghost_1.png').convert_alpha()
        ghost_2 = pygame.image.load('/Users/chirathrashmika/Desktop/Pixel_ghost/graphics/ghost_2.png').convert_alpha()
        self.ghost_walk = [ghost_1, ghost_2]
        self.ghost_index = 0
        self.ghost_jump = pygame.image.load('/Users/chirathrashmika/Desktop/Pixel_ghost/graphics/ghost_1_up.png').convert_alpha()

        self.image = self.ghost_walk[self.ghost_index]
        self.rect = self.image.get_rect(midbottom = (150,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('/Users/chirathrashmika/Desktop/Pixel_ghost/music/swing-whoosh-110410.ogg')
        self.jump_sound.set_volume(0.8)


    def ghost_input(self):
         keys = pygame.key.get_pressed()
         if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -15
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 0.5
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animating_ghost(self):
        if self.rect.bottom < 300:
            self.image = self.ghost_jump
        else:
            self.ghost_index += 0.1
            if self.ghost_index >= len(self.ghost_walk):
                self.ghost_index = 0
            self.image = self.ghost_walk[int(self.ghost_index)]


    def update(self):
        self.ghost_input()
        self.apply_gravity()
        self.animating_ghost()

class Obstacles(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()    
        
        if type == 'bat1':
            bat_frame1 = pygame.image.load('/Users/chirathrashmika/Desktop/Pixel_ghost/graphics/bat1.png').convert_alpha()
            bat_frame2 = pygame.image.load('/Users/chirathrashmika/Desktop/Pixel_ghost/graphics/bat2.png').convert_alpha()
            self.bat_frames = [bat_frame1, bat_frame2]
            y_pos = 200
        else:
            bat_frame1 = pygame.image.load('/Users/chirathrashmika/Desktop/Pixel_ghost/graphics/bat1.png').convert_alpha()
            bat_frame2 = pygame.image.load('/Users/chirathrashmika/Desktop/Pixel_ghost/graphics/bat2.png').convert_alpha()
            self.bat_frames = [bat_frame1, bat_frame2]
            y_pos = 290

        self.animation_index = 0
        self.image = self.bat_frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def bat_animation(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.bat_frames):
            self.animation_index = 0
        self.image = self.bat_frames[int(self.animation_index)]  

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
    
    def update(self):
        self.bat_animation()
        self.rect.x -= 8
        self.destroy()
    
def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = text_font.render(f'Score: {current_time}' , True, 'black' )
    score_rect = score_surf.get_rect(midbottom = (400, 380))
    screen.blit(score_surf,score_rect)
    return current_time
    
def display_game_over():
    game_over = text_font.render(f'GAME OVER', False, 'black')
    game_over = pygame.transform.scale2x(game_over)
    game_over_rect = game_over.get_rect(midbottom = (400,200))
    if game_active == False:
        screen.blit(game_over, game_over_rect)

def display_game_start():
    start = text_font.render(f'press Space to start', True, 'black')
    start_rect = start.get_rect(midbottom = (400,250))
    if game_active == False:
        screen.blit(start,start_rect)

def collision_sprite():
    crash_sound = pygame.mixer.Sound('/Users/chirathrashmika/Desktop/Pixel_ghost/music/ani-big-pipe-hit-6814.ogg')
    crash_sound.set_volume(0.3)
    if pygame.sprite.spritecollide(ghost.sprite, obstacle_group, False):
        obstacle_group.empty()
        crash_sound.play()
        return False
    else:
        return True 
        
def lake_animation():
    global lake_surf, lake_frame_index

    if game_active:
        lake_frame_index += 0.05
        if lake_frame_index >= len(lake_frames):
            lake_frame_index = 0
        lake_surf = lake_frames[int(lake_frame_index)]    
   
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Pixel Ghost')
clock = pygame.time.Clock()
text_font = pygame.font.Font(None, 50)
game_active = False
start_time = 0
score = 0
background_music = pygame.mixer.Sound('/Users/chirathrashmika/Desktop/Pixel_ghost/music/creepy-music-box-halloween-music-horror-scary-spooky-dark-ambient-118577.ogg')
background_music.set_volume(0.1)
background_music.play(loops = -1)

#groups
ghost = pygame.sprite.GroupSingle()
ghost.add(Ghost())

obstacle_group = pygame.sprite.Group()


sky_surf = pygame.image.load('/Users/chirathrashmika/Desktop/Pixel_ghost/graphics/background-1.png').convert()

lake_frame1 = pygame.image.load('/Users/chirathrashmika/Desktop/Pixel_ghost/graphics/lake 1.png').convert()
lake_frame2 = pygame.image.load('/Users/chirathrashmika/Desktop/Pixel_ghost/graphics/lake 2.png').convert()
lake_frames = [lake_frame1, lake_frame2]
lake_frame_index = 0
lake_surf = lake_frames[lake_frame_index]

obstacle_rect_list = []

ghost_1 = pygame.image.load('/Users/chirathrashmika/Desktop/Pixel_ghost/graphics/ghost_1.png').convert_alpha()
ghost_2 = pygame.image.load('/Users/chirathrashmika/Desktop/Pixel_ghost/graphics/ghost_2.png').convert_alpha()
ghost_walk = [ghost_1, ghost_2]
ghost_index = 0
ghost_jump = pygame.image.load('/Users/chirathrashmika/Desktop/Pixel_ghost/graphics/ghost_1_up.png').convert_alpha()

ghost_surf = ghost_walk[ghost_index]
ghost_rect = ghost_surf.get_rect(bottomright =(180,300))
ghost_grav = 0

game_over_background = pygame.image.load('/Users/chirathrashmika/Desktop/Pixel_ghost/graphics/game_over.png').convert()
game_sart_background = pygame.image.load('/Users/chirathrashmika/Desktop/Pixel_ghost/graphics/game_start.png').convert()

#timer
obstacle_timer1 = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer1, randint(1050,3000))

obstacle_timer2 = pygame.USEREVENT + 2
pygame.time.set_timer(obstacle_timer2, randint(900,1300))

bat_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(bat_animation_timer,200)


async def main():

    while True:

        global game_active,score

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if game_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and ghost_rect.bottom >= 300:
                        ghost_grav = -15
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_active = True
                        start_time = int(pygame.time.get_ticks()/1000)
            
            if game_active:
                if score <= 1000:
                    if event.type == obstacle_timer1:
                        obstacle_group.add(Obstacles(choice(['bat1', 'bat2', 'bat2', 'bat2'])))
                else:
                    if event.type == obstacle_timer2:
                        obstacle_group.add(Obstacles(choice(['bat1', 'bat2', 'bat2', 'bat2'])))

        if game_active:
            
            
            screen.blit(sky_surf,(0,0))
            
            lake_animation()
            screen.blit(lake_surf, (0,300))
            score = display_score()

            ghost.draw(screen)
            ghost.update()

            obstacle_group.draw(screen)
            obstacle_group.update()


            #collision
            game_active = collision_sprite()
            
        else:
            if score == 0:
                screen.blit(game_sart_background,(0,0))
                display_game_start()
            else:    
                screen.blit(game_over_background,(0,0))
                score_massage = text_font.render(f'Your Score: {score}', False, 'black')
                score_massage_rect = score_massage.get_rect(center = (400,330))
                screen.blit(score_massage, score_massage_rect) 
                display_game_over()
            
            obstacle_rect_list.clear()

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())        