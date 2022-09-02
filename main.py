import pygame
from sys import exit
import random

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk1,player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (200,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.2)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= groundLevel:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
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
    def __init__(self, type):
        super().__init__()
        
        if type == 'fly':
            fly_frame1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_frame2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_frame1,fly_frame2]
            y_pos = random.choice([groundLevel - 90,groundLevel - 35]) 
        else:
            snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame1,snail_frame2]
            y_pos = groundLevel

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (random.randint(900,1100),y_pos))
        self.speed = 8

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= self.speed
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score(font, startTime):
    currentTime = int((pygame.time.get_ticks() - startTime) / 100) 
    score_surf = font.render(f'Score: {currentTime}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,75))
    screen.blit(score_surf,score_rect)
    return currentTime

def display_highScore(font, highScore):
    highScore_surf = font.render(f'High Score: {highScore}',False,(64,64,64))
    highScore_rect = highScore_surf.get_rect(center = (400,25))
    screen.blit(highScore_surf,highScore_rect)

def sprite_collision():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:
        return True

pygame.init()

#VARIABLES
displayWidth = 800
displayHeight = 400
groundLevel = 300
maxFrameRate = 60
game_active = False
startTime = 0

tempHighScore = 0
have_highScore = False
score = 0

clock = pygame.time.Clock()
screen = pygame.display.set_mode((displayWidth,displayHeight))
pygame.display.set_caption('Pee Pee Poo Poo')
font = pygame.font.Font('font/Pixeltype.ttf',50)
music = pygame.mixer.Sound('Audio/music.wav')
music.set_volume(0.01)

#GROUPS
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

#BACKGROUND
sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/Ground.png').convert_alpha()

#INTRO SCREEN
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand.get_rect(center = (400,200))
game_name = font.render('The Pee Pee Poo Poo Run',True,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,310))
game_message = font.render('Press space to run',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400, 350))

fail_message = font.render('GAME OVER',True,(64,64,64))
fail_message_rect1 = fail_message.get_rect(center = (150, 150))
fail_message_rect2 = fail_message.get_rect(center = (650, 150))

#TIMER
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,900)

#GAME LOOP
while True:
    music.play(loops = -1)
    #EVENT LOOP
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(random.choice(['fly','snail','snail'])))
        else: 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                startTime = pygame.time.get_ticks()

    if game_active:
        #BACKGROUND
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,groundLevel))

        #SCORE
        score = display_score(font, startTime)

        #SPRITES
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()

        #COLLISION
        if sprite_collision() == False:
            currentHighScore = score
            game_active = False
            have_highScore = True

        #SCORING
        if have_highScore: 
            if currentHighScore > tempHighScore:
                display_highScore(font,currentHighScore)
                tempHighScore = currentHighScore
            else:
                display_highScore(font,tempHighScore)
             
    else:
        #WAITING SCREEN
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        player.midbottom = (80,300)
        screen.blit(game_name,game_name_rect)
        screen.blit(game_message,game_message_rect)

        #GAME OVER SCREEN
        if score != 0:
            if currentHighScore > tempHighScore:
                display_highScore(font,currentHighScore)
                tempHighScore = currentHighScore
            else:
                display_highScore(font,tempHighScore)
            score_message = font.render(f'Your Score: {score}',False,(111,196,169))
            score_message_rect = score_message.get_rect(center = (400,75))
            screen.blit(score_message,score_message_rect)
            screen.blit(fail_message,fail_message_rect1)
            screen.blit(fail_message,fail_message_rect2)
        
    pygame.display.update()
    clock.tick(maxFrameRate)