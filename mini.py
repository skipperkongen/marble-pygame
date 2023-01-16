"""
Remake of the veritcal stack demo from the box2d testbed.
"""

import math

import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse

import pymunk
from pymunk import Vec2d
import pymunk.pyglet_util

SPAWN_X = 70
SPAWN_Y = 400
SIDE1_X = 50
SIDE2_X = 550
GAP = 100
INCLINE = 20
SIZE = 1
SPAWN_FREQ = 10
FRICTION = 0.0001

class Main(pyglet.window.Window):
    def __init__(self):

        pyglet.window.Window.__init__(self, vsync=False)
        self.set_caption('Minimal example')

        pyglet.clock.schedule_interval(self.update, 1/60.0)
        pyglet.clock.schedule_interval(self.spawn, 1.0/SPAWN_FREQ)
        self.fps_display = pyglet.window.FPSDisplay(self)

        self.text = pyglet.text.Label('Fafis og Dudus verden',
                          font_size=10,
                          x=10, y=400)
        self.create_world()

        self.draw_options = pymunk.pyglet_util.DrawOptions()
        self.draw_options.flags = self.draw_options.DRAW_SHAPES

    def create_world(self):
        self.space = pymunk.Space()
        self.space.gravity = Vec2d(0.,-900.)
        self.space.sleep_time_threshold = 0.3

        static_lines = [
            # sides
            pymunk.Segment(self.space.static_body, Vec2d(SIDE1_X,55), Vec2d(SIDE1_X,400), 1),
            pymunk.Segment(self.space.static_body, Vec2d(SIDE2_X,55), Vec2d(SIDE2_X,400), 1),
        ]
        for i in range(1, 4):
            x1 = SIDE1_X
            x2 = SIDE2_X - GAP
            y1 = SPAWN_Y - GAP*i
            y2 = SPAWN_Y - GAP*i - INCLINE
            floor1 = pymunk.Segment(self.space.static_body, Vec2d(x1, y1), Vec2d(x2, y2), 1)
            floor2 = pymunk.Segment(self.space.static_body, Vec2d(x1+GAP, y2-GAP/2), Vec2d(x2+GAP, y1-GAP/2), 1)
            static_lines.append(floor1)
            static_lines.append(floor2)


        for l in static_lines:
            l.friction = FRICTION
        self.space.add(static_lines)

    def update(self, dt):
        # Here we use a very basic way to keep a set space.step dt.
        # For a real game its probably best to do something more complicated.
        step_dt = 1/250.
        x = 0
        while x < dt:
            x += step_dt
            self.space.step(step_dt)

    def spawn(self, dt):
        mass = 200
        r = SIZE
        moment = pymunk.moment_for_circle(mass, 0, r, (0,0))
        body = pymunk.Body(mass, moment)
        body.position = (SPAWN_X, SPAWN_Y)
        shape = pymunk.Circle(body, r, (0,0))
        shape.friction = FRICTION
        shape.color = (255,150,150,255)
        self.space.add(body, shape)
        f = 100
        body.apply_impulse_at_local_point((f,0), (0,0))


    # def on_key_press(self, symbol, modifiers):
    #     if symbol == key.SPACE:
    #         mass = 100
    #         r = 15
    #         moment = pymunk.moment_for_circle(mass, 0, r, (0,0))
    #         body = pymunk.Body(mass, moment)
    #         body.position = (0, 165)
    #         shape = pymunk.Circle(body, r, (0,0))
    #         shape.friction = 0.3
    #         shape.color = (255,150,150,255)
    #         self.space.add(body, shape)
    #         f = 200000
    #         body.apply_impulse_at_local_point((f,0), (0,0))
    #     elif symbol == key.ESCAPE:
    #         pyglet.app.exit()
    #     elif symbol == pyglet.window.key.P:
    #         pyglet.image.get_buffer_manager().get_color_buffer().save('box2d_vertical_stack.png')


    def on_draw(self):
        self.clear()
        self.text.draw()
        self.fps_display.draw()
        self.space.debug_draw(self.draw_options)

if __name__ == '__main__':
    main = Main()
    pyglet.app.run()
