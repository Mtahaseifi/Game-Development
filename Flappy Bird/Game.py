import arcade
import time
from random import randint
import json as js
import os

COUNT_TOP_PIPE = 20
COUNT_DOWN_PIPE = 20
GRAVITY = 0.3
BIRD_JUMP_SPEED = 7

class Game(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, 'Flappy Bird')

        self.bg = arcade.Sprite('images/bg.png', 3)
        self.bg.center_x = width // 2
        self.bg.center_y = height // 2

        self.h = arcade.load_sound('sounds/Game-Over-Sound-Effect-4.mp3')
        self.bird = Bird()
        self.pipe_list = []
        self.best_score = 0

        self.game_over = False
        self.game_over_sprite = arcade.Sprite('images/gameover-removebg-preview.png')
        self.game_over_sprite.center_x = 400
        self.game_over_sprite.center_y = 200

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.bird,
            gravity_constant=GRAVITY
        )

    def setup(self):
        self.bird.center_y = 300
        self.pipe_list = []
        self.score = 0
        self.start_time = time.time()
        if not os.path.exists('best_score.json'):
            with open('best_score.json', "w", encoding="utf-8") as f:
                js.dump([] , f )

    def on_draw(self):

        self.clear()
        arcade.draw_sprite(self.bg)

        for p in self.pipe_list:
            p.display()

        arcade.draw_sprite(self.bird)

        arcade.draw_text(f"Score: {self.score}", 10, self.height - 30, arcade.color.UA_RED, 20)
        arcade.draw_text(f"Best Score: {self.best_score}", self.width-180, self.height - 30, arcade.color.UA_RED, 20)        

        if self.game_over:
            arcade.draw_sprite(self.game_over_sprite)
            
    def on_update(self, delta_time):
        
        self.physics_engine.update()

        if self.game_over:
            return
            
        if time.time() - self.start_time > 1:
            pipe = Pipes(x=1000)
            self.pipe_list.append(pipe)
            self.start_time = time.time()

        for p in self.pipe_list:
            p.update_x()
            if p.bot_pipe.center_x < 0:
                p.remove_from_sprite_list()
                self.pipe_list.remove(p)
                self.score += 1  
        
        for p in self.pipe_list:
            if arcade.check_for_collision(self.bird, p.bot_pipe) or arcade.check_for_collision(self.bird, p.top_pipe):
                arcade.play_sound(self.h)
                with open('best_score.json','r+',encoding="utf-8") as f:
                    data = js.load(f)
                    data.append(self.score)
                    f.seek(0)
                    js.dump(data,f)
                self.game_over = True  

        if self.bird.center_y < 0:
            arcade.play_sound(self.h)
            self.game_over = True  
            with open('best_score.json','r+',encoding="utf-8") as f:
                data = js.load(f)
                data.append(self.score)
                f.seek(0)
                js.dump(data,f)

        with open('best_score.json','r',encoding="utf-8") as f:
                scores = js.load(f)
                if scores :
                    self.best_score = max(scores)
                elif not scores:
                    self.best_score = 0

    def on_key_press(self, key, modifiers):
        if self.game_over == False:
            if self.bird.center_y < 390:
                if key == arcade.key.SPACE:
                    self.bird.change_y = BIRD_JUMP_SPEED


class Bird(arcade.Sprite):
    def __init__(self):
        super().__init__('images/bird-removebg-preview.png', 0.3)
        self.center_x = 100
        self.center_y = 300  


class Pipes:
    def __init__(self, x):

        self.top_pipe = arcade.Sprite('images/pipe2-removebg-preview.png')
        self.bot_pipe = arcade.Sprite('images/pipe1-removebg-preview.png')

        self.bot_pipe.center_x = x
        self.top_pipe.center_x = x

        self.bot_pipe.center_y = randint(-100, 100)
        self.top_pipe.center_y = self.bot_pipe.center_y + 400

    def display(self):
       arcade.draw_sprite(self.top_pipe)
       arcade.draw_sprite(self.bot_pipe)

    def update_x(self):
        self.bot_pipe.center_x -= 5
        self.top_pipe.center_x -= 5

    def remove_from_sprite_list(self):
        self.bot_pipe.remove_from_sprite_lists()
        self.top_pipe.remove_from_sprite_lists()

if __name__ == '__main__':
    game = Game(800, 400)
    game.setup()
    arcade.run()