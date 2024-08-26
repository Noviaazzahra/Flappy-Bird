# Import Modul
import pygame
import sys
import random

# Inisialisasi Pygame
pygame.init()

# konstanta
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GROUND_HEIGHT = SCREEN_HEIGHT - 70
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 200  # Jarak vertikal antara pipa
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# untuk memasukan gambar ke dalam game
background_img = pygame.image.load('C:\\Users\\Rara\\OneDrive\\Documents\\FLAPPY BIRD\\flappy-bird-background-gecj5m4a9yhhjp87.jpg')
bird_img = pygame.image.load('C:\\Users\\Rara\\OneDrive\\Documents\\FLAPPY BIRD\\burung.png')
pipe_img = pygame.image.load('C:\\Users\\Rara\\OneDrive\\Documents\\FLAPPY BIRD\\pipa.png')

# Set ukuran gambar burung
bird_img = pygame.transform.scale(bird_img, (BIRD_WIDTH, BIRD_HEIGHT))
pipe_img = pygame.transform.scale(pipe_img, (PIPE_WIDTH, PIPE_HEIGHT))

# Fungsi untuk menggambar teks
def draw_text(surface, text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

# Fungsi menu utama
def main_menu(screen):
    while True:
        screen.blit(background_img, (0, 0))
        draw_text(screen, 'Flappy Bird', 60, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        draw_text(screen, 'Press SPACE to Start', 30, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

# Fungsi utama game
def game_loop(screen):
    clock = pygame.time.Clock()
    bird_x = SCREEN_WIDTH // 4
    bird_y = SCREEN_HEIGHT // 2
    bird_velocity = 0
    bird_flap_strength = -10
    gravity = 0.5
    
    # Buat beberapa pipa
    pipe_count = 4
    pipes = []
    pipe_spacing = SCREEN_WIDTH // (pipe_count + 1) + 100  # Perlebar jarak antara pipa
    
    for i in range(pipe_count):
        pipe_x = SCREEN_WIDTH + i * pipe_spacing
        pipe_y = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        pipes.append({'x': pipe_x, 'y': pipe_y, 'passed': False})
    
    pipe_velocity = -4
    score = 0
    game_over = False
    
    while True:
        screen.blit(background_img, (0, 0))
        
        if game_over:
            draw_text(screen, f'Game Over! Score: {score}', 50, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)
            draw_text(screen, 'Press SPACE to Restart', 30, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            draw_text(screen, 'Press Q to Quit', 30, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird_velocity = bird_flap_strength
            
            bird_velocity += gravity
            bird_y += bird_velocity
            
            # Update posisi pipa
            for pipe in pipes:
                pipe['x'] += pipe_velocity
            
            # Tambah pipa baru dan hapus pipa yang keluar dari layar
            if pipes[0]['x'] < -PIPE_WIDTH:
                pipes.pop(0)
                new_pipe_x = pipes[-1]['x'] + pipe_spacing
                new_pipe_y = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
                pipes.append({'x': new_pipe_x, 'y': new_pipe_y, 'passed': False})
            
            # Periksa benturan
            bird_rect = pygame.Rect(bird_x, bird_y, BIRD_WIDTH, BIRD_HEIGHT)
            for pipe in pipes:
                top_pipe_rect = pygame.Rect(pipe['x'], pipe['y'] - PIPE_HEIGHT, PIPE_WIDTH, PIPE_HEIGHT)
                bottom_pipe_rect = pygame.Rect(pipe['x'], pipe['y'] + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - (pipe['y'] + PIPE_GAP))
                
                if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
                    game_over = True
                    break

            if bird_y > GROUND_HEIGHT or bird_y < 0:
                game_over = True
            
            # Periksa apakah burung melewati pipa
            for pipe in pipes:
                if pipe['x'] + PIPE_WIDTH < bird_x and not pipe['passed']:
                    score += 1
                    pipe['passed'] = True

            # Gambar burung dan pipa
            screen.blit(bird_img, (bird_x, bird_y))
            for pipe in pipes:
                screen.blit(pipe_img, (pipe['x'], pipe['y'] - PIPE_HEIGHT))
                screen.blit(pipe_img, (pipe['x'], pipe['y'] + PIPE_GAP))
            
            draw_text(screen, f'Score: {score}', 30, BLACK, SCREEN_WIDTH // 2, 30)
            
            pygame.display.flip()
            clock.tick(30)

# Main
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Flappy Bird')
    while True:
        main_menu(screen)
        game_loop(screen)

if __name__ == "__main__":
    main()
