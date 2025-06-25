import os
os.environ['SDL_VIDEO_CENTERED'] = '1'
import random
import pygame
import math

WIDTH = 1200
HEIGHT = 700

# ------------ GAME STATE --------------
class Game: pass
game = Game()
game.status = "revive"
game.t = 0.01
game.v0 = 100
game.v1 = 60
game.bg = 0
game.level = 1
game.pause = False

bg = ['sfondo1', 'livello1', 'livello2', 'livello3']

sounds.soundtrack.play(-1)

# ------------ COMMON ACTORS & BOXES --------------
oca = Actor('oca')
oca.pos = (558, 550)
oca.step = 7
oca.vy = 0
oca.on_ground = True
oca_facing_right = True

box4 = pygame.Rect((1050, 600), (100, 100))
box5 = pygame.Rect((520, 500), (60, 60))
box_x = 500
box_y = 435
box_size = (147, 47)
box = Rect((box_x, box_y), box_size)
box1_size = (55, 20)
box1 = pygame.Rect((1077, 568), box1_size)
box2_size = (85, 35)
box2 = pygame.Rect((1065, 640), box2_size)

# ------------ LEVEL ONE --------------
actors = []
game.points_1 = 0
game.lives_1 = 3
game.gameover_1 = False

def spawn_random_actor():
    if game.gameover_1 or game.level == 2:
        return
    kind = random.choice(['osso', 'cervello_fresco', 'cervello_avariato'])
    actor = Actor(kind)
    actor.v = game.v0 + game.points_1 // 15 * 10
    actor.x = random.randint(actor.width, WIDTH - actor.width)
    actor.y = 0 + actor.height/2
    actors.append(actor)

clock.schedule_interval(spawn_random_actor, 1.3)

def level_one():
    fall()
    update_one()

def update_one():
    if game.gameover_1 or game.pause or game.level == 2:
        return
    for actor in actors[:]:
        if actor.y > HEIGHT:
            if actor.image == 'cervello_fresco':
                miss(actor)
            actors.remove(actor)
        elif oca.colliderect(actor):
            eat(actor)
            actors.remove(actor)
            if game.points_1 >= 115:
                sounds.victory.play()
                game.level = 2

def fall():
    if game.gameover_1 or game.pause or game.level == 2:
        return
    for actor in actors:
        actor.y += actor.v * game.t

def miss(actor):
    if actor.image == 'cervello_fresco':
        game.lives_1 -= 1
        if game.lives_1 <= 0:
            game.gameover_1 = True
            sounds.gameover.play()

def eat(actor):
    if actor.image == 'cervello_fresco':
        game.points_1 += 15
        sounds.points.play()
    elif actor.image == 'cervello_avariato':
        game.points_1 -= 5
        sounds.nopoints.play()
    elif actor.image == 'osso':
        game.points_1 -= 10
        sounds.nopoints.play()

def reset_one():
    global actors
    actors = []
    game.points_1 = 0
    game.lives_1 = 3
    game.gameover_1 = False
    game.pause = False
    game.level = 1

# ------------ LEVEL TWO --------------
GROUND_Y = 550
GRAVITY = 0.7
JUMP_VELOCITY = -22
OBSTACLE_SPEED = 4
MAX_SCORE = 4000
oca.is_jumping = False

obstacles = []
game_over_two = False
score = 0
oca_damage = 115
level_completed = False

def reset_two():
    global obstacles, oca, game_over_two, score, oca_damage, level_completed
    oca.pos = (180, GROUND_Y)
    oca.vy = 0
    oca.is_jumping = False
    obstacles = []
    game_over_two = False
    score = 0
    oca_damage = 115
    level_completed = False
    game.pause = False

def level_two():
    update_two()

def update_two():
    global game_over_two, score, oca_damage, level_completed
    if game_over_two or level_completed or game.pause:
        return
    if score >= MAX_SCORE:
        level_completed = True
        sounds.victory.play()
        return

    if oca.is_jumping:
        oca.vy += GRAVITY
        oca.y += oca.vy
        sounds.quack.play()
        if oca.y >= GROUND_Y:
            oca.y = GROUND_Y 
            oca.is_jumping = False
            oca.vy = 0

    for obs in obstacles:
        obs.x -= OBSTACLE_SPEED
    obstacles[:] = [obs for obs in obstacles if obs.right > 0]
    if len(obstacles) == 0 or obstacles[-1].x < WIDTH - random.randint(350, 750):
        kind = random.choice(['gnomo_rosso', 'gnomo_blu'])
        if kind == 'gnomo_rosso':
            red_gnome = Actor('gnomo_rosso')
            red_gnome.midbottom = (WIDTH + 40, GROUND_Y + 55)
            red_gnome.danno = 8
            red_gnome.tipo = "rosso"
            obstacles.append(red_gnome)
        else:
            blu_gnome = Actor('gnomo_blu')
            blu_gnome.midbottom = (WIDTH + 40, GROUND_Y + 55)
            blu_gnome.danno = 4
            blu_gnome.tipo = "blu"
            obstacles.append(blu_gnome)

    for obs in obstacles[:]:
        if oca.colliderect(obs):
            oca_damage -= obs.danno
            sounds.nopoints.play()
            obstacles.remove(obs)
            if oca_damage <= 0:
                game_over_two = True
                sounds.gameover.play()
                oca_damage = 0
    score += 1

# ------------ LEVEL THREE --------------
# Variabili e attori specifici del livello 3
oca3 = Actor('oca')
oca3.pos = (200, 550)
oca3.step = 15
oca3.vy = 0
oca3.on_ground = True
oca3_facing_right = True
oca3_vite = 5

batticarne = Actor('batticarne')
bimbo = Actor('boss_normale')
bimbo_base_x = 980
bimbo_base_y = 470
bimbo.x = bimbo_base_x
bimbo.y = bimbo_base_y
bimbo.image = 'boss_normale'

bimbo_flash_timer = 0
bimbo_stage = 0
cervello = Actor('cervellobambinomutante')
cervello.visible = False

titoli_coda = [
    "FINE",
    "Complimenti, avete superato tutti i livelli!",
    "Ora l'oca radioattiva puo' riposare in pace...",
    "e con lo stomaco pieno (del cervello del bimbo minchia)",
    "",
    "Codice - Maria Elena Pela'",
    "Audio - Valeria De Piccoli, Alessia Formigari",
    "Sfondo - Alessia Formigari",
    "Actors - Annachiara Amadessi",
    "Livelli - Nor Es sadeqy",
    "Presentazione - Nor Es sadeqy, Valeria De Piccoli",
    "Design Document - Valeria De Piccoli",
    "",
    "Grazie per aver giocato",
    "a RADIOACTIVE GOOSE"
]
titoli_offset_y = HEIGHT

proiettili = []
batticarne_colpi = []
batticarne_ready = True

fase_gioco = 1
colpi_al_bimbo = 0

def level_three_draw():
    screen.blit('livello3', (0, 0))
    global titoli_offset_y
    if fase_gioco == 1:
        oca3.draw()
        batticarne.draw()
        for p in proiettili:
            p.draw()
        bimbo.draw()
        for colpo in batticarne_colpi:
            colpo.draw()
        screen.draw.text(f"VENDETTA - Vite: {oca3_vite}", (50, 30), color=(255,255,250), fontsize=32,fontname='pixel', owidth=1, ocolor="black")
        #screen.draw.text("Colpisci il bambino con il batticarne! (x5)", (50, 58), color="red",fontname='pixel', fontsize=24)
        if oca3_vite <= 0:
            screen.draw.text("GAME OVER!", (330, 245), color="red",fontname='pixel', fontsize=150)
            screen.draw.text("Premi R per riprovare", (460,355), color="red",fontname='pixel', fontsize=42)
    elif fase_gioco == 2:
        oca3.draw()
        if cervello.visible:
            cervello.draw()
        screen.draw.text("Hai sconfitto il bambino! Ora prendi il cervello...", (50, 20), color="white",fontname='pixel', fontsize=32)
        screen.draw.text(f"Vite rimaste: {oca3_vite}", (50, 60), color="white",fontname='pixel', fontsize=26)
    elif fase_gioco == 3:
        screen.fill((0,10,25))
        oca3.draw()
        y = titoli_offset_y
        for riga in titoli_coda:
            screen.draw.text(riga, (80, y), color="white", fontsize=20, fontname='pixel',owidth=2, ocolor="black")
            y += 45

def flip_actor(actor):
    actor._surf = pygame.transform.flip(actor._surf, True, False)

def level_three_update():
    global fase_gioco, bimbo_flash_timer, titoli_offset_y
    if fase_gioco == 1:
        fase1_update()
    elif fase_gioco == 2:
        fase2_update()
    elif fase_gioco == 3:
        fase3_update()
    if bimbo_flash_timer > 0:
        bimbo_flash_timer -= 1 / 60
        if bimbo_flash_timer <= 0:
            if bimbo_stage == 0:
                bimbo.image = 'boss_normale'
            else:
                bimbo.image = 'boss_finale'

def fase1_update():
    global oca3_facing_right, colpi_al_bimbo, oca3_vite, fase_gioco, bimbo, batticarne_ready, bimbo_flash_timer, bimbo_stage
    if oca3_vite <= 0:
        if keyboard.r:
            reset_livello3()
            sounds.gameover.play()
        return
    if keyboard.right and oca3.x < WIDTH - oca3.width / 1.4:
        oca3.x += oca3.step
        if not oca3_facing_right:
            flip_actor(oca3)
            flip_actor(batticarne)
            oca3_facing_right = True
    elif keyboard.left and oca3.x > 0 + oca3.width / 1.4:
        oca3.x -= oca3.step
        if oca3_facing_right:
            flip_actor(oca3)
            flip_actor(batticarne)
            oca3_facing_right = False
    if keyboard.up and oca3.on_ground:
        oca3.vy = -22
        oca3.on_ground = False
    if not oca3.on_ground:
        oca3.y += oca3.vy
        oca3.vy += 1
        ground_y = 550
        if oca3.y >= ground_y:
            oca3.y = ground_y
            oca3.vy = 0
            oca3.on_ground = True
    offset_x = 40
    offset_y = -30
    if oca3_facing_right:
        batticarne.x = oca3.x + offset_x
    else:
        batticarne.x = oca3.x - offset_x
    batticarne.y = oca3.y + offset_y
    bimbo.x = bimbo_base_x
    bimbo.y = bimbo_base_y + 60 * math.sin(pygame.time.get_ticks() / 600)
    for p in proiettili[:]:
        p.x += p.vx
        p.y += p.vy
        if oca3.colliderect(p):
            proiettili.remove(p)
            oca3_vite -= 1
            if oca3_vite <= 0:
                return
        if p.right < 0 or p.x > WIDTH:
            proiettili.remove(p)
    if keyboard.z and batticarne_ready:
        spara_batticarne()
        sounds.batticarne.play()
        batticarne_ready = False
    if not keyboard.z:
        batticarne_ready = True
    for colpo in batticarne_colpi[:]:
        colpo.x += colpo.vx
        if colpo.x < 0 or colpo.x > WIDTH:
            batticarne_colpi.remove(colpo)
        elif colpo.colliderect(bimbo):
            colpi_al_bimbo += 1
            batticarne_colpi.remove(colpo)
            if colpi_al_bimbo < 2:
                bimbo_stage = 0
                bimbo.image = 'boss_normale_rosso'
            elif colpi_al_bimbo == 2:
                bimbo_stage = 1
                bimbo.image = 'boss_finale_rosso'
            elif colpi_al_bimbo == 3:
                bimbo_stage = 1
                bimbo.image = 'boss_finale_rosso'
            elif colpi_al_bimbo == 4:
                bimbo_stage = 1
                bimbo.image = 'boss_finale_rosso'
            elif colpi_al_bimbo == 5:
                bimbo_stage = 1
                bimbo.image = 'boss_finale_rosso'
            bimbo_flash_timer = 0.15
            if colpi_al_bimbo == 2:
                bimbo_stage = 1
            if colpi_al_bimbo >= 5:
                sounds.victory.play()
                fase_gioco = 2

def fase2_update():
    global fase_gioco, oca3_facing_right
    cervello.visible = True
    cervello.pos = (1000, 550)
    moving = False
    if keyboard.right and oca3.x < WIDTH - oca3.width / 1.4:
        oca3.x += oca3.step
        if not oca3_facing_right:
            flip_actor(oca3)
            oca3_facing_right = True
        moving = True
    elif keyboard.left and oca3.x > 0 + oca3.width / 1.4:
        oca3.x -= oca3.step
        if oca3_facing_right:
            flip_actor(oca3)
            oca3_facing_right = False
        moving = True
    if moving:
        oca3.image = "oca_corre"
        oca3.y = 573
    else:
        oca3.image = "oca"
        oca3.y = 550
    if oca3.colliderect(cervello):
        oca3.image = "oca"
        sounds.crock.play()
        fase_gioco = 3
        cervello.visible = False
        if oca3_facing_right:
            oca3.x += 20
            flip_actor(oca3)
            oca3_facing_right = False

def fase3_update():
    global titoli_offset_y
    if titoli_offset_y > -1200:
        titoli_offset_y -= 1.1
        
    sounds.soundtrack.stop()

def spara_batticarne():
    if fase_gioco == 1 and oca3_vite > 0:
        direzione = 1 if oca3_facing_right else -1
        colpo = Actor('batticarne')
        colpo.pos = (oca3.x, oca3.y - 30)
        colpo.vx = 50 * direzione
        batticarne_colpi.append(colpo)

def spara_proiettile():
    if fase_gioco == 1 and oca3_vite > 0:
        proiettile = Actor('proiettile', center=(820,550))
        proiettile.vx = -random.randint(8, 12)
        proiettile.vy = random.randint(-3, 3)
        proiettili.append(proiettile)
clock.schedule_interval(spara_proiettile, 0.7)

def reset_livello3():
    global proiettili, batticarne_colpi, colpi_al_bimbo, fase_gioco, cervello, oca3_vite, titoli_offset_y, oca3_facing_right, batticarne_ready, bimbo_flash_timer, bimbo_stage
    proiettili.clear()
    batticarne_colpi.clear()
    colpi_al_bimbo = 0
    oca3.pos = (200, 550)
    oca3.on_ground = True
    oca3_facing_right = True
    batticarne.pos = (oca3.x + 40, oca3.y - 30)
    fase_gioco = 1
    cervello.visible = False
    oca3_vite = 5
    titoli_offset_y = HEIGHT
    bimbo.image = 'boss_normale'
    bimbo.x = bimbo_base_x
    bimbo.y = bimbo_base_y
    batticarne_ready = True
    bimbo_flash_timer = 0
    bimbo_stage = 0
#-----------STORIA-----------
storia = []
storia = [

    "1986. Pochi mesi dopo il disastro nucleare di Chernobyl,",
    "l'Unione Sovietica diede inizio a operazioni di bonifica nella zona di esclusione.",
    "Tra gli ordini impartiti ai soldati:",
    "abbattere tutti gli animali superstiti",
    "per prevenire la diffusione di contaminazioni.",
    "",
    "Durante una battuta, un'oca viene colpita a morte...",
    "ma la contaminazione nucleare fa il suo corso.",
    "Anni dopo, il suo corpo, sepolto e mutato, viene disturbato dal canto stonato",
    "di un bambino mutante, generato dalle stesse radiazioni.",
    "",
    "Ora risorta come oca zombie, armata di un batticarne arrugginito,",
    "la protagonista intraprende una folle missione di vendetta.",
    "Il bambino fugge nella foresta lasciando strane impronte",
    "(un piede normale, uno zoccolo caprino):",
    "l'oca dovra' seguirle attraverso i paesaggi devastati della foresta.",

]
storia_offset_y = HEIGHT
# ------------ DRAW & INPUT --------------

def draw():
    global box1, oca, box2
    if game.status == "revive":
        screen.clear()
        screen.blit(bg[game.bg], (0, 0))
        box = Rect((2000, 2000), box_size)
        screen.draw.filled_rect(box, (85,40,0))
        screen.draw.text("START", (5305,3097), color="brown",fontname='pixel', fontsize=65)
        screen.draw.text("?", (540, 530), color = "white",fontname='pixel', fontsize = 60,owidth=1, ocolor="black")
    elif game.status == "storia":
        screen.clear()
        screen.fill((0, 10,20))
        screen.draw.text("Next", (1070, 640), color="white",fontname='pixel', fontsize=30)
        y = storia_offset_y
        for riga in storia:
            screen.draw.text(riga, (80, y), color="white", fontsize=25, fontname='pixel',owidth=2, ocolor="black")
            y += 45
    elif game.status == "start":
        screen.clear()
        screen.blit(bg[game.bg], (0, 0))
        screen.blit('casella', (0,-30))
        box = Rect((box_x, box_y), box_size)
        oca.draw()
        screen.draw.text("Radioactive", (340,225), color="white",fontname='pixel', fontsize=90)
        screen.draw.text("goose", (470,320), color="white",fontname='pixel', fontsize=90)
        screen.draw.filled_rect(box, (0,0,0))
        screen.draw.text("START", (515,445), color="white",fontname='pixel', fontsize=35)
    elif game.status == "level one":
        screen.clear()
        screen.blit(bg[game.bg], (0, 0))
        oca.draw()
        if not game.gameover_1 and game.level != 2:
            for actor in actors:
                actor.draw()
        screen.draw.text("Points: " + str(game.points_1), (1055, 35), color="white",fontname='pixel', fontsize=30)
        screen.draw.text("Lives: " + str(game.lives_1), (1055, 65), color="white",fontname='pixel', fontsize=30)
        if game.gameover_1:
            screen.draw.text("GAME OVER", (330, 245), color="white",fontname='pixel', fontsize=100)
            screen.draw.text("Press 'R' to reset", (460, 355), color="white",fontname='pixel', fontsize=40)
        if game.level == 2:
            screen.draw.filled_rect(box1, (175, 170, 180))
            screen.draw.text("Next", (1083, 570), color="black",fontname='pixel', fontsize=20)
    elif game.status == "level two":
        screen.clear()
        screen.blit(bg[game.bg], (0, 0))
        box1 = Rect((2800, 1140), box1_size)
        oca.draw()
        for obs in obstacles:
            obs.draw()
        screen.draw.text(f"Score: {score // 10}", topright=(WIDTH - 40, 25),fontname='pixel', fontsize=36, color="white")
        screen.draw.text(f"Attack damage: {oca_damage}", topleft=(30, 25), fontname='pixel',fontsize=36, color="white")
        screen.blit('porta',(0,0))
        if game_over_two:
            screen.draw.text("GAME OVER", (330, 245),fontname='pixel', fontsize=64, color="white")
            screen.draw.text("Premi R per riprovare", (460, 355),fontname='pixel', fontsize=36, color="white")
        if level_completed:
            screen.draw.text("LIVELLO COMPLETATO!", center=(WIDTH//2, HEIGHT//2 - 30),fontname='pixel', fontsize=64, color="white",owidth=0.1, ocolor="black")
            screen.draw.filled_rect(box2, (175, 170, 180))
            screen.draw.text("Next",(1072,645), color="black", fontname='pixel',fontsize=30)
    elif game.status == "level three":
        level_three_draw()

def on_key_down(key):
    global oca
    if game.status in ("start", "level one", "level two"):
        if key == keys.SPACE:
            game.pause = not game.pause
    if game.status == "level one":
        if key == keys.R and game.gameover_1:
            reset_one()
    if game.status == "level two":
        if key == keys.UP:
            if not oca.is_jumping and not game_over_two and not level_completed:
                oca.is_jumping = True
                oca.vy = JUMP_VELOCITY
        elif key == keys.R:
            if game_over_two or level_completed:
                reset_two()
    if game.status == "level three":
        # Nel livello 3 la gestione dei comandi è nella logica level_three_update
        pass

def update_oca_move():
    global oca, oca_facing_right
    moved = False
    if keyboard.right and oca.x < WIDTH - oca.width/1.4:
        oca.x += oca.step
        if not oca_facing_right:
            flip_actor(oca)
            oca_facing_right = True
        moved = True
    elif keyboard.left and oca.x > 0 + oca.width/1.4:
        oca.x -= oca.step
        if oca_facing_right:
            flip_actor(oca)
            oca_facing_right = False
        moved = True

def update():
    global storia_offset_y
    if game.status == "start":
        game.bg = 0
        update_oca_move()
    if game.status == "storia":
        if storia_offset_y > -1200:
            storia_offset_y -= 1.1
    elif game.status == "level one":
        game.bg = 1
        level_one()
        update_oca_move()
    elif game.status == "level two":
        game.bg = 2
        oca.x = 250
        level_two()
    elif game.status == "level three":
        game.bg = 3
        level_three_update()

def on_mouse_down(pos):
    global oca
    if game.status == "revive":
        if box5.collidepoint(pos):
            print("Cliccato '?'")
            game.status = "storia"
    elif game.status=="storia":
        if box4.collidepoint(pos):
            print("Cliccato 'box4'")
            game.status = "start"
    elif game.status == "start":
        if box.collidepoint(pos):
            print("Cliccato START")
            sounds.quack.play()
            game.status = "level one"
            oca.image= 'oca_mangia'
    elif game.status == "level one" and game.level == 2:
        if box1.collidepoint(pos):
            print("Cliccato NEXT da level one a level two")
            game.status = "level two"
            oca.image= 'oca'
    elif game.status == "level two":
        if box2.collidepoint(pos):
            print("Cliccato NEXT da level two a level three")
            game.status = "level three"
            # Reset livello 3!
            reset_livello3()