import arcade
import random

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SNAKE_SIZE = 30
SPEED = 0.1
COUNT_PEAR = 10
COUNT_APPLE = 10
COUNT_BOMB = 5
COUNT_HEART = 5

class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Snake Game")
        self.snake = Snake()
        self.tslm = 0

        self.bg = arcade.Sprite('images/bg_snake.png', 4)
        self.bg.center_x = SCREEN_WIDTH // 2
        self.bg.center_y = SCREEN_HEIGHT // 2

        self.pear_list = arcade.SpriteList()
        self.apple_list = arcade.SpriteList()
        self.bomb_list = arcade.SpriteList()
        self.heart_list = arcade.SpriteList()

        self.fruit_li = []
        self.game_over = False 
        self.go_sprite = arcade.Sprite('images\play_again-removebg-preview.png',1.3)
        self.winner_sprite = arcade.Sprite('images/winner_sprite-removebg-preview.png')

        self.go_sprite.center_x = SCREEN_WIDTH//2
        self.go_sprite.center_y = SCREEN_HEIGHT//2

        self.winner_sprite.center_x = SCREEN_WIDTH//2
        self.winner_sprite.center_y = SCREEN_HEIGHT//2
        
        self.eating_sound = arcade.load_sound('sounds/heavy_swallowwav-14682.mp3')
        self.lose_sound = arcade.load_sound('sounds/Game-Over-Sound-Effect-4.mp3')
        self.hit_sound = arcade.load_sound('sounds\Exclamation Sound effect.mp3')
        self.game_over = False
        

    def setup(self):
        
        self.game_over = False
        self.lives = 5

        self.apple_list.clear()
        self.pear_list.clear()
        self.bomb_list.clear()
        self.fruit_li.clear()

        for _ in range(COUNT_PEAR):

            pear = Pear()
            pear.center_x = random.randint(10, SCREEN_WIDTH)
            pear.center_y = random.randint(10, SCREEN_HEIGHT)
            self.pear_list.append(pear)
            self.fruit_li.append(pear)
        

        for _ in range(COUNT_APPLE):
            apple = Apple()
            apple.center_x = random.randint(10, SCREEN_WIDTH)
            apple.center_y = random.randint(10, SCREEN_HEIGHT)
            self.apple_list.append(apple)
            self.fruit_li.append(apple)

        for _ in range(COUNT_BOMB):
            bomb = Bomb()
            bomb.center_x = random.randint(10, SCREEN_WIDTH)
            bomb.center_y = random.randint(10, SCREEN_HEIGHT)
            self.bomb_list.append(bomb)

        for i in range(COUNT_HEART):
            heart = arcade.Sprite('images/heart-removebg-preview.png',0.5)
            heart.center_x = 30+i*50
            heart.center_y = 550
            self.heart_list.append(heart)

    def on_draw(self):
        self.clear()
        arcade.draw_sprite(self.bg)
        self.snake.display()
        arcade.draw_sprite(self.head_sprite)

        self.pear_list.draw()
        self.apple_list.draw()
        self.bomb_list.draw()
        self.heart_list.draw()

        if self.game_over:
            arcade.draw_sprite(self.go_sprite)
            # arcade.draw_text('play again? y/n',100,500,arcade.color.YELLOW_ROSE,50)

        if len(self.fruit_li) <=0:
            arcade.draw_sprite(self.winner_sprite)

    def on_update(self, delta_time):

        if not self.game_over and len(self.fruit_li) >0: 
            self.tslm += delta_time
            if self.tslm >= SPEED:
                self.snake.move()
                self.tslm = 0 
            
            head_x, head_y = self.snake.body[0] 
            self.head_sprite = arcade.Sprite('images/head3-removebg-preview.png', 0.3)  
            self.head_sprite.center_x, self.head_sprite.center_y = head_x, head_y

            for bomb in self.bomb_list:
                if arcade.check_for_collision(self.head_sprite, bomb):  

                    bomb.remove_from_sprite_lists()
                    arcade.play_sound(self.hit_sound)
            
                    if len (self.heart_list) >=0 :
                        self.heart_list.pop(-1)

                    self.lives-=1
                    if self.lives <=0 :
                        arcade.play_sound(self.lose_sound)
                        self.game_over = True

            for p in self.pear_list:
                if arcade.check_for_collision(self.head_sprite,p):
                    p.remove_from_sprite_lists()
                    self.fruit_li.pop()
                    self.snake.body.append(((self.snake.body[-1])[0]-20,(self.snake.body[-1])[1]))
                    arcade.play_sound(self.eating_sound)

            for a in self.apple_list:
                if arcade.check_for_collision(self.head_sprite,a):
                    a.remove_from_sprite_lists()
                    self.fruit_li.pop()
                    self.snake.body.append(((self.snake.body[-1])[0]-20,(self.snake.body[-1])[1]))
                    arcade.play_sound(self.eating_sound)

    def on_key_press(self, key, modifires):

        if self.game_over == False  :
            if key == arcade.key.UP:
                self.snake.change_direction((0, SNAKE_SIZE))
            elif key == arcade.key.DOWN:
                self.snake.change_direction((0, -SNAKE_SIZE))
            elif key == arcade.key.LEFT:
                self.snake.change_direction((-SNAKE_SIZE, 0))
            elif key == arcade.key.RIGHT:
                self.snake.change_direction((SNAKE_SIZE, 0))

        elif self.game_over == True or len(self.fruit_li) <= 0:
            if key == arcade.key.Y:
                self.setup()
                self.snake = Snake() 
            
            elif key == arcade.key.N:
                arcade.close_window()

class Snake:
    def __init__(self):

        self.body = [(100, 100), ]  
        self.direction = (SNAKE_SIZE, 0)  

    def move(self):
        head_x, head_y = self.body[0] 
        new_head = (head_x + self.direction[0], head_y + self.direction[1]) 
        self.body.insert(0, new_head) 
        self.body.pop(-1) 

    def change_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def display(self):
        for segment in self.body:
            arcade.draw_circle_filled(segment[0], segment[1], SNAKE_SIZE // 2, arcade.color.GREEN_YELLOW)

class Fruite(arcade.Sprite):
    def __init__(self, path, size):
        super().__init__(path, size)

class Apple(Fruite):
    def __init__(self):
        super().__init__('images/apple.png', 0.3)
        
class Pear(Fruite):
    def __init__(self):
        super().__init__('images/pear.png', 0.3)
    
class Bomb(arcade.Sprite):
    def __init__(self):
        super().__init__('images/bomb.png', 0.3)

if __name__ == "__main__":
    game = Game()
    game.setup()
    arcade.run()