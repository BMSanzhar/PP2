import pygame
import random
import psycopg2
from sys import exit

# PostgreSQL байланысы
conn = psycopg2.connect(
    host="localhost",
    dbname="snake_db",
    user="postgres",
    password="87277478111",
    port="5432"
)
cur = conn.cursor()

pygame.init()

# Экран параметрлері
WIDTH = 800
HEIGHT = 600
BLOCK_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

# Түстер
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Шрифт
font = pygame.font.Font(None, 36)

# Ойын параметрлері
clock = pygame.time.Clock()
score = 0
level = 1

# ------------------------
def get_or_create_user(username):
    cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    if user:
        return user[0]
    else:
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
        conn.commit()
        return cur.fetchone()[0]

def get_user_progress(user_id):
    cur.execute("SELECT score, level FROM user_score WHERE user_id = %s ORDER BY id DESC LIMIT 1", (user_id,))
    return cur.fetchone()

def generate_apple(snake):
    while True:
        x = random.randint(0, (WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE
        y = random.randint(0, (HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE
        if (x, y) not in snake:
            return x, y

# ------------------------
def main():
    global score, level

    username = input("🧑 Enter your username: ")
    user_id = get_or_create_user(username)
    progress = get_user_progress(user_id)
    if progress:
        score, level = progress
        speed = 10 + (level - 1) * 2
        print(f"👋 Welcome back, {username}! Continuing from Level {level} with Score {score}")
    else:
        score, level, speed = 0, 1, 10
        print(f"👋 Welcome, {username}! Starting a new game.")


    # Генерируем змейку с длиной, соответствующей score
    snake = []
    head_x, head_y = 300, 300
    for i in range(3 + score):  # начальная длина + 1 блок за каждый фрукт
        snake.append((head_x - i * BLOCK_SIZE, head_y))



    direction = "RIGHT"
    food = generate_apple(snake)
    running = True

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    print("⏸️ Game paused. Saving progress...")
                    cur.execute("INSERT INTO user_score (user_id, score, level) VALUES (%s, %s, %s)", (user_id, score, level))
                    conn.commit()
                    pygame.time.wait(500)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and direction != "DOWN":
            direction = "UP"
        elif keys[pygame.K_DOWN] and direction != "UP":
            direction = "DOWN"
        elif keys[pygame.K_LEFT] and direction != "RIGHT":
            direction = "LEFT"
        elif keys[pygame.K_RIGHT] and direction != "LEFT":
            direction = "RIGHT"

        head_x, head_y = snake[0]
        if direction == "UP":
            head_y -= BLOCK_SIZE
        elif direction == "DOWN":
            head_y += BLOCK_SIZE
        elif direction == "LEFT":
            head_x -= BLOCK_SIZE
        elif direction == "RIGHT":
            head_x += BLOCK_SIZE

        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT or (head_x, head_y) in snake:
            running = False

        snake.insert(0, (head_x, head_y))

        if (head_x, head_y) == food:
            score += 1
            if score % 4 == 0:
                level += 1
                speed += 2
            food = generate_apple(snake)
        else:
            snake.pop()

        for part in snake:
            pygame.draw.rect(screen, GREEN, (part[0], part[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, RED, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))

        score_txt = font.render(f"Score: {score} Level: {level}", True, WHITE)
        screen.blit(score_txt, (10, 10))

        pygame.display.flip()
        clock.tick(speed)

    # Ойын біткен соң
    cur.execute("INSERT INTO user_score (user_id, score, level) VALUES (%s, %s, %s)", (user_id, score, level))
    conn.commit()

    final_score = font.render(f"Your score: {score}    Your level: {level}", True, WHITE)
    game_over_text = font.render("Game Over! Press any key to exit", True, WHITE)
    screen.fill(BLACK)
    screen.blit(final_score, (240, 200))
    screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False
                pygame.quit()
                exit()

# ------------------------
main()
