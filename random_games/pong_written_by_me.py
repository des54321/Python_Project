import pygame as pg

pg.init()
window_size = (600, 400)
screen = pg.display.set_mode(window_size)
pg.display.set_caption('Pong')
paddle_width = 15
paddle_height = 60
ball_size = 20
ball_x = window_size[0] / 2 - ball_size / 2
ball_y = window_size[1] / 2 - ball_size / 2
ball_vx = 3
ball_vy = 3
paddle1_x = 20
paddle1_y = window_size[1] / 2 - paddle_height / 2
paddle2_x = window_size[0] - 20 - paddle_width
paddle2_y = window_size[1] / 2 - paddle_height / 2
paddle_speed = 5
black = (0, 0, 0)
white = (255, 255, 255)
font = pg.font.Font(None, 36)
score1 = 0
score2 = 0
running = True
clock = pg.time.Clock()
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    ball_x += ball_vx
    ball_y += ball_vy
    if ball_y < 0 or ball_y > window_size[1] - ball_size:
        ball_vy = -ball_vy
    if ball_x < 0:
        score2 += 1
        ball_x = window_size[0] / 2 - ball_size / 2
        ball_y = window_size[1] / 2 - ball_size / 2
        ball_vx = -ball_vx
    if ball_x > window_size[0] - ball_size:
        score1 += 1
        ball_x = window_size[0] / 2 - ball_size / 2
        ball_y = window_size[1] / 2 - ball_size / 2
        ball_vx = -ball_vx
    if ball_x < paddle1_x + paddle_width and ball_y > paddle1_y and ball_y < paddle1_y + paddle_height:
        ball_vx = -ball_vx
    if ball_x > paddle2_x and ball_y > paddle2_y and ball_y < paddle2_y + paddle_height:
        ball_vx = -ball_vx
    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        paddle1_y = max(0, paddle1_y - paddle_speed)
    if keys[pg.K_s]:
        paddle1_y = min(window_size[1] - paddle_height, paddle1_y + paddle_speed)
    if keys[pg.K_UP]:
        paddle2_y = max(0, paddle2_y - paddle_speed)
    if keys[pg.K_DOWN]:
        paddle2_y = min(window_size[1] - paddle_height, paddle2_y + paddle_speed)
    screen.fill(black)
    pg.draw.rect(screen, white, (paddle1_x, paddle1_y, paddle_width, paddle_height))
    pg.draw.rect(screen, white, (paddle2_x, paddle2_y, paddle_width, paddle_height))
    pg.draw.circle(screen, white, (int(ball_x), int(ball_y)), ball_size // 2)

    # Render the score
    score_text1 = font.render(str(score1), True, white)
    score_text2 = font.render(str(score2), True, white)
    screen.blit(score_text1, (window_size[0] / 2 - 50, 20))
    screen.blit(score_text2, (window_size[0] / 2 + 30, 20))

    # Update the display
    pg.display.flip()

    # Limit the frame rate to 60 FPS
    clock.tick(60)
