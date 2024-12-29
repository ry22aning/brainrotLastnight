import pygame
import time
import random
pygame.font.init()
pygame.mixer.init() 

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("THAT FEELING WHEN KNEE SURGERY IS TMRW")

BG = pygame.image.load("x.jpg")

PLAYER_WIDTH = 70
PLAYER_HEIGHT = 65
PLAYER_VEL = 5
PLAYER_IMG = pygame.image.load("kneeImg.webp")
PLAYER_IMG = pygame.transform.scale(PLAYER_IMG, (PLAYER_WIDTH, PLAYER_HEIGHT)) 


FONT = pygame.font.SysFont("comicsans", 20)

STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3

def main():
    run = True
    #skibiddi_msgs = []

    stars = []
    hit = False

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()
    
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    #SKIBIDDI MUSSIKK
    pygame.mixer.music.load("kneeFeeling.mp3")
    pygame.mixer.music.play(-1) #for loop
    

    while run:
        star_count += clock.tick(60) #max no of FPS, no of time while loop runs
        elapsed_time = time.time() - start_time
        time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        
        WIN.blit(BG, (0, 0))
        WIN.blit(time_text, (5,5))

        WIN.blit(PLAYER_IMG, (player.x, player.y))
        
        #to draw collisions
        for star in stars:
            pygame.draw.rect(WIN, "white", star)

        # Update the display
        pygame.display.update()

        #KEYS SKIBIDDI TOILET MOVEMENT
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL
        if keys[pygame.K_UP] and player.y - PLAYER_VEL >= 0: 
            player.y -= PLAYER_VEL
        if keys[pygame.K_DOWN] and player.y + PLAYER_VEL + player.height <= HEIGHT:  
            player.y += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            pygame.mixer.music.stop() 
            pygame.time.delay(4000)
            NEWBG = pygame.image.load("bala.jpg")
            lost_text = FONT.render("Your code is ass write it again!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2 ))
            pygame.mixer.music.load("subha.mp3")
            pygame.mixer.music.play(-1)
            pygame.display.update()
            break


    pygame.quit()

if __name__ == "__main__":
    main()