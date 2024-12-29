import pygame
import time
import random
import cv2  
import numpy as npfi

pygame.font.init()
pygame.mixer.init()

# Window dimensions
WIDTH, HEIGHT = 1050, 655
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("That feeling when knee surgery is tmrw")

BG = pygame.image.load("x3.jpg")

#SKIBIDDI configuration
PLAYER_WIDTH = 75
PLAYER_HEIGHT = 65
PLAYER_VEL = 5
PLAYER_IMG = pygame.image.load("kneeImg.webp")
PLAYER_IMG = pygame.transform.scale(PLAYER_IMG, (PLAYER_WIDTH, PLAYER_HEIGHT))

FONT = pygame.font.SysFont("comicsans", 20)

#KNEE CONF
STAR_WIDTH = 50
STAR_HEIGHT = 50
STAR_VEL = 3
STAR_IMG = pygame.image.load("orgKnee.jpeg")
STAR_IMG = pygame.transform.scale(STAR_IMG, (STAR_WIDTH, STAR_HEIGHT))


def play_video(video_path):
    """Plays a video using OpenCV on the left side of the screen."""
    cap = cv2.VideoCapture(video_path)

    # Video audio handling is done by pygame's mixer, so we need to load audio separately
    pygame.mixer.music.load("sonic_music.mp3")  # You may need to extract the audio from the video manually
    pygame.mixer.music.play(-1)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame = cv2.resize(frame, (WIDTH // 2, HEIGHT))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = pygame.surfarray.make_surface(frame)

        WIN.blit(frame, (0, 0))
        pygame.display.update()

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    run = True
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
    pygame.mixer.music.play(-1)

    while run:
        star_count += clock.tick(60) 
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
        WIN.blit(time_text, (5, 5))
        WIN.blit(PLAYER_IMG, (player.x, player.y))

        for star in stars:
            WIN.blit(STAR_IMG, (star.x, star.y))
            
        #Update the display
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
            elif star.colliderect(player):
                hit = True
                break

        if hit:
            pygame.mixer.music.stop()
            break

    if hit:
        play_video("sonic.mp4")  

    pygame.quit()


if __name__ == "__main__":
    main()
