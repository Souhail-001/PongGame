import pygame
import math
pygame.init()

W , H  = 900 , 700

win = pygame.display.set_mode((W,H))
pygame.display.set_caption("Ping Pong")

fps = 50

white = (255,255,255)
black = (0,0,0) 
orange = (255,165,0)
green  =  (0,255,0)

Paddle_W , Paddle_H = 12 , 110
BALL_RADIUS = 10
Circle_RADIUS = 180

SCORE_FONT = pygame.font.SysFont("comicsans", 50)
bot_FONT = pygame.font.SysFont("comicsans", 50)
INFO_FONT = pygame.font.SysFont("comicsans", 28)
WINNING_SCORE = 5

class Ball:
    MAX_VEL = 10
    COLOR = orange

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        pygame.time.delay(700)
        self.y_vel = 0
        self.x_vel *= -1

class Circle:
    COLOR = white

    def __init__(self,x,y,radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, win):
        pygame.draw.arc(win, self.COLOR, 
                (self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2), 0, math.pi*2, 2) 
        
class bot_paadle:
    color = white
    D = 6

    def __init__(self,x,y,W,H):
        self.x = self.original_x = x
        self.y = self.original_y = y 
        self.W = W
        self.H = H

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.W, self.H))


    def move(self,up=True):
        if up:
            self.y -= self.D
        else:
            self.y += self.D
    
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

class paddle:
    color = white
    D = 6

    def __init__(self,x,y,W,H):
        self.x = self.original_x = x
        self.y = self.original_y = y 
        self.W = W
        self.H = H

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.W, self.H))


    def move(self,up=True):
        if up:
            self.y -= self.D
        else:
            self.y += self.D
    
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


def draw(win, paddles, ball, left_score, right_score,circle):
    win.fill(black)

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, white)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, white)
    win.blit(left_score_text, (W//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (W * (3/4) -right_score_text.get_width()//2, 20))

    circle.draw(win)

    for paddle in paddles:
        paddle.draw(win)
    j = 1
    for i in range(10, H, H//25):
        j+=1
        if j % 2 == 1:
            continue
        pygame.draw.rect(win, white, (W//2 - 5, i, 5, H//20))
    
    ball.draw(win)

    hint = INFO_FONT.render("Left: W/S    Right: ↑/↓    Pause: P", True, (120,120,120))
    win.blit(hint, (15, H - 30))
    pygame.display.update()

   
def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= H:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.H:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.W:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.H / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.H / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.H:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.H / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.H / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

class first_game:
    status = True

def maintain_bot(difficulty):
    win.fill(black)
    bot_option1 = bot_FONT.render("Press e for easy bot", True, (220,220,220))
    win.blit(bot_option1, ((W - bot_option1.get_width())//2, H//2 - 30))
    bot_option2 = bot_FONT.render("Press h for hard bot", True, (220,220,220))
    win.blit(bot_option2, ((W - bot_option2.get_width())//2, H//2 + bot_option1.get_height() ))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        waiting = False
                        break
                    if event.key == pygame.K_h:
                        waiting = False
                        difficulty = True
                        break    

def main():
    win.fill(black)
    flag = True
    bot_option1 = bot_FONT.render("Press b to play vs Bot", True, (220,220,220))
    win.blit(bot_option1, ((W - bot_option1.get_width())//2, H//2 -30))
    bot_option2 = bot_FONT.render("Press m for Multiplayer", True, (220,220,220))
    win.blit(bot_option2, ((W - bot_option2.get_width())//2, H//2 + bot_option1.get_height() ))
    pygame.display.update()
    waiting = True
    difficulty = False
    while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        waiting = False
                        break
                    if event.key == pygame.K_b:
                        waiting = False
                        flag = False
                        maintain_bot(difficulty)
                        break


    run = True
    paused = False
    clock = pygame.time.Clock()
    left_paddle = paddle(10, H//2 - Paddle_H // 2, Paddle_W, Paddle_H)
    right_paddle = paddle(W - 10 - Paddle_W, H // 2 - Paddle_H//2, Paddle_W, Paddle_H)
    ball = Ball(W // 2, H // 2, BALL_RADIUS)
    circle = Circle(W//2,H//2,Circle_RADIUS)

    left_score = 0
    right_score = 0

    while run:
        clock.tick(fps)
        draw(win, [left_paddle, right_paddle], ball, left_score, right_score,circle)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    break
                if event.key == pygame.K_SPACE :
                    main()
                if event.key == pygame.K_p:
                    paused = not paused

        keys = pygame.key.get_pressed()
        if not paused:
            if flag:
                if keys[pygame.K_s] and left_paddle.y - left_paddle.D >= 0:
                    left_paddle.move(up=True)
                if keys[pygame.K_w] and left_paddle.y + left_paddle.D + left_paddle.H <= H:
                    left_paddle.move(up=False)
            else:
                if difficulty:
                     if ball.y < left_paddle.y and left_paddle.y - left_paddle.D >= 0:
                         left_paddle.move(up=True)
                     if ball.y > (left_paddle.y + 110) and left_paddle.y + left_paddle.D + left_paddle.H <= H:
                         left_paddle.move(up=False)
                else:
                    if ball.y < left_paddle.y and ball.x < W//2 and left_paddle.y - left_paddle.D >= 0:
                         left_paddle.move(up=True)
                    if ball.y > (left_paddle.y + 110) and ball.x < W//2 and left_paddle.y + left_paddle.D + left_paddle.H <= H:
                         left_paddle.move(up=False)

            if keys[pygame.K_UP] and right_paddle.y - right_paddle.D >= 0:
                right_paddle.move(up=True)
            if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.D + right_paddle.H <= H:
                right_paddle.move(up=False)

            ball.move()
            handle_collision(ball, left_paddle, right_paddle)

        if ball.x < -ball.radius:
            right_score += 1
            ball.reset()
        elif ball.x > W+ball.radius:
            left_score += 1
            ball.reset()

        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"

        if won:
            first_game.status = False
            left_score_text = SCORE_FONT.render(f"{left_score}", 1, green)
            right_score_text = SCORE_FONT.render(f"{right_score}", 1, green)
            win.blit(left_score_text, (W//2 - left_score_text.get_width()//2 - 40, H//2 - 100))
            win.blit(right_score_text, (W //2 -right_score_text.get_width()//2 + 40, H//2 - 100))

            text = SCORE_FONT.render(win_text, 1, green)
            win.blit(text, (W//2 - text.get_width() //2, H//2 - text.get_height()//2))

            info = INFO_FONT.render("Press ENTER to restart or ESC to quit.", True, (220,220,220))
            win.blit(info, ((W - info.get_width())//2, H//2 + 30))
            pygame.display.update()
            waiting = True
            while waiting:
              for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                      pygame.quit()
                      exit()
                  if event.type == pygame.KEYDOWN:
                      if event.key == pygame.K_ESCAPE:
                          exit()
                      if event.key == pygame.K_RETURN:
                          waiting = False
                          ball.reset()
                          left_paddle.reset()
                          right_paddle.reset()
                          left_score = 0
                          right_score = 0
                          main()
               
    pygame.QUIT


if __name__ == '__main__':
    main()