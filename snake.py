import pygame
from random import randint
from pygame.locals import *

TURQUOISE = (64, 224, 208)
GREEN = (60, 242, 71)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLOCK_SIZE = 20

class App:
        
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 600, 600
        self.clock = pygame.time.Clock()
        self.snake = None
        self.fruit = None

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.snake = Square_snake(5, 5, YELLOW, self._display_surf)
        self.fruit = Snake_fruit(randint(0, 29), randint(0, 29), TURQUOISE, self._display_surf)
    
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    
    def on_loop(self):
        if self.snake.body[0] == (self.fruit.x, self.fruit.y):
            while True:
                new_fruit_x, new_fruit_y = randint(0, 29), randint(0, 29)
                if (new_fruit_x, new_fruit_y) not in self.snake.body:
                    break
            self.fruit = Snake_fruit(new_fruit_x, new_fruit_y, TURQUOISE, self._display_surf)
            self.snake.grow()



    def on_render(self):
        self._display_surf.fill(BLACK)
        self.snake.draw()
        self.fruit.draw()
        self.snake.update()
        self.draw_lines()
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def draw_lines(self):
        block_size = 20
        for x in range(0, self.width, block_size):
            for y in range(0, self.height, block_size):
                rect = pygame.Rect(x, y, block_size, block_size)
                pygame.draw.rect(self._display_surf, GREEN, rect, 1 )




    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        
        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.snake.handle_keys()
            self.on_render()
            
            self.clock.tick(10)
        self.on_cleanup()


class Square_snake():
    def __init__(self, x, y, color, surface):
            self.x = x
            self.y = y
            self.color = color
            self.surface = surface
            #self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
            #self.image.fill(self.color)
            #self.rect = self.image.get_rect(topleft=(self.x * BLOCK_SIZE, self.y * BLOCK_SIZE))
            self.direction = "RIGHT" 
            self.body = [(x, y)]
        
    def draw(self):
        #self.surface.blit(self.image, self.rect)
        for tail in self.body:
            rect = pygame.Rect(tail[0] * BLOCK_SIZE, tail[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(self.surface, self.color, rect)
    
    def update(self):
        head_x, head_y = self.body[0]


        if self.direction == "LEFT":
            head_x -= 1
        elif self.direction == "RIGHT":
            head_x += 1
        elif self.direction == "UP":
            head_y -= 1
        elif self.direction == "DOWN":
            head_y += 1

        #adding loop collision
        head_x %= 30
        head_y %= 30

        self.body.insert(0, (head_x, head_y))
        self.body.pop()
        
    def grow(self):
        self.body.append(self.body[-1])


    def handle_keys(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT] and self.direction != "RIGHT": 
            self.direction = "LEFT" 
        if key[pygame.K_RIGHT] and self.direction != "LEFT":
            self.direction = "RIGHT"
        if key[pygame.K_UP] and self.direction != "DOWN":
            self.direction = "UP"
        if key[pygame.K_DOWN] and self.direction != "UP":
            self.direction = "DOWN"

class Snake_fruit():
    def __init__(self, x, y, color, surface):
        self.x = x
        self.y = y
        self.color = color
        self.surface = surface
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=(self.x * BLOCK_SIZE, self.y * BLOCK_SIZE))
    
    def draw(self):
        self.surface.blit(self.image, self.rect)
        
    def update(self):
        self.rect.topleft = (self.x * BLOCK_SIZE, self.y * BLOCK_SIZE)





if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()

