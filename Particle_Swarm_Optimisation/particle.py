import random
import math
import numpy as np # optional
import turtle
from time import sleep as delay
import copy

def ackley(x1,x2): # optional
    a = 20
    b = 0.2
    c = 2*np.pi
    
    sum1 = x1**2 + x2**2 
    sum2 = np.cos(c*x1) + np.cos(c*x2)
    
    term1 = - a * np.exp(-b * ((1/2.) * sum1**(0.5)))
    term2 = - np.exp((1/2.)*sum2)

    return term1 + term2 + a + np.exp(1)

def six_hump_fun(x,y):
    z = (4-2.1*(x**2)+(x**4)/3)*(x**2) + x*y + (-4+4*(y**2))*(y**2)
    return z

def obj_fun(x,y):
    return six_hump_fun(x,y)


class Position:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Velocity:
    def __init__(self,v_x,v_y):
        self.x = v_x
        self.y = v_y

class Solution:
    def __init__(self,x,y):
        self.position = Position(x,y)
        self.cost = math.inf

    def update_cost(self):
        self.cost = obj_fun(self.position.x,self.position.y)
    

class Particle:
    def __init__(self,pos,vel,inertia_weight,c1,c2,v_max,pos_range,show_animation):
        self.position = Position(pos.x,pos.y) # this needs to be passed in as a position
        self.velocity = Velocity(vel.x,vel.y) # this needs to be passed in as a velocity
        self.weight = inertia_weight
        self.c1 = c1
        self.c2 = c2
        self.v_max = v_max # this is max v for individual x or y axis, so technically max velocity is sqrt(2)*v_max
        self.pbest = Solution(pos.x,pos.y) 
        self.pbest.update_cost()
        self.gbest = Solution(pos.x,pos.y)
        self.prev_gbest = Solution(pos.x,pos.y)
        self.cur_cost = self.pbest.cost
        self.pos_range = pos_range
        self.show_animation = show_animation
        self.p = 1
        self.success = 0
        self.failure = 0
        self.is_gbest = False
        self.first_being_gbest = True
        self.e_s = 7 # half of the document values
        self.e_f = 3 
        if self.show_animation:
            self.turtleboy = turtle.Turtle()
            # self.turtleboy.penup()
            self.turtleboy.turtlesize(0.3,0.3)
            self.turtleboy.speed(5)
            self.turtleboy.shape("turtle")


    def update_velocity_weight(self):
        r1_x = random.random()
        r1_y = random.random()
        r2_x = random.random()
        r2_y = random.random()
        self.velocity.x = self.weight*self.velocity.x \
                            + self.c1*r1_x*(self.pbest.position.x - self.position.x) \
                            + self.c2*r2_x*(self.gbest.position.x - self.position.x)
        self.velocity.y = self.weight*self.velocity.y \
                            + self.c1*r1_y*(self.pbest.position.y - self.position.y) \
                            + self.c2*r2_y*(self.gbest.position.y - self.position.y)
        if self.velocity.x > self.v_max:
            self.velocity.x = self.v_max
        if self.velocity.y > self.v_max:
            self.velocity.y = self.v_max

    def update_velocity_constr(self):
        r1_x = random.random()
        r1_y = random.random()
        r2_x = random.random()
        r2_y = random.random()
        phi = self.c1+self.c2
        if phi <= 4.1:
            phi = 4.1
            K = 0.729843
        else:
            K = 2/abs(2-phi-math.sqrt(phi**2 - 4*phi))

        self.velocity.x = K*(self.velocity.x \
                            + self.c1*r1_x*(self.pbest.position.x - self.position.x) \
                            + self.c2*r2_x*(self.gbest.position.x - self.position.x))
        self.velocity.y = K*(self.velocity.y \
                            + self.c1*r1_y*(self.pbest.position.y - self.position.y) \
                            + self.c2*r2_y*(self.gbest.position.y - self.position.y))
        if self.velocity.x > self.v_max:
            self.velocity.x = self.v_max
        if self.velocity.y > self.v_max:
            self.velocity.y = self.v_max

    def update_velocity_guaren(self):
        if not(self.is_gbest): # this means normal update rule
            self.update_velocity_weight()
            self.first_being_gbest = True
        else: # this means we are on the special particle
            self.update_p_scaling()
            r2_x = random.random()
            r2_y = random.random()

            self.velocity.x = -self.position.x + self.gbest.position.x + self.weight*self.velocity.x \
                                + self.p*(1-2*r2_x)
            self.velocity.y = -self.position.y + self.gbest.position.y + self.weight*self.velocity.y \
                                + self.p*(1-2*r2_y)
            if self.velocity.x > self.v_max:
                self.velocity.x = self.v_max
            if self.velocity.y > self.v_max:
                self.velocity.y = self.v_max

    def update_p_scaling(self):
        if self.first_being_gbest: # means this is the first time p_scaling is done
            self.first_being_gbest = False
            self.p = 1 # this is setting up the parameters
            self.success = 0
            self.failure = 0
            self.prev_gbest = copy.deepcopy(self.gbest)
        else:
            if self.prev_gbest.position.x == self.gbest.position.x \
                and self.prev_gbest.position.y == self.gbest.position.y: # this means a failure
                self.failure = self.failure + 1
                self.success = 0
            else: # this means a success
                self.success = self.success + 1
                self.failure = 0
                self.prev_gbest = copy.deepcopy(self.gbest)
            if self.success > self.e_s:
                self.p = self.p*2
            elif self.failure > self.e_f:
                self.p = self.p/2

    def update_position(self):
        self.position.x = self.position.x + self.velocity.x
        self.position.y = self.position.y + self.velocity.y
        if self.position.x < self.pos_range[0]:
            self.position.x = self.pos_range[0]
        elif self.position.x > self.pos_range[1]:
            self.position.x = self.pos_range[1]
        if self.position.y < self.pos_range[0]:
            self.position.y = self.pos_range[0]
        elif self.position.y > self.pos_range[1]:
            self.position.y = self.pos_range[1]

    def update_pbest(self):
        self.cur_cost = obj_fun(self.position.x,self.position.y)
        if self.cur_cost < self.pbest.cost:
            self.pbest.position = copy.copy(self.position)
            self.pbest.cost = self.cur_cost
        self.pbest.position.x = self.position.x
        self.pbest.position.y = self.position.y
        return self.cur_cost

    def animate(self):
        if self.show_animation:
            self.turtleboy.clear()
            # self.turtleboy.penup()
            self.turtleboy.turtlesize(0.3,0.3)
            self.turtleboy.speed(5)
            self.turtleboy.goto(self.position.x,self.position.y)



    

if __name__ == "__main__":
    # print(obj_fun(0.089,-0.71))
    # birdie1 = Particle(Position(0,0),Velocity(0,0),0,0,0,0,[-5,5])
    # birdie1.cur_cost = 1
    # birdie1.pbest.cost = 2
    # print(birdie1.pbest.cost)
    # print(birdie1.cur_cost)
    # birdie1.cur_cost = 3
    # print(birdie1.pbest.cost)
    # print(birdie1.cur_cost)
    # print(obj_fun(0.31,19.35))
    turtle.setworldcoordinates(-5,-5,5,5)
    turtle.tracer(1000,100)
    screen = turtle.Screen()
    birdie1 = Particle(Position(0,0),Velocity(0,0),0,0,0,0,[-5,5],True)
    birdie2 = Particle(Position(0,0),Velocity(0,0),0,0,0,0,[-5,5],True)
    for i in range(0,100):
        birdie1.position.x = random.randint(-5,5)
        birdie1.position.y = random.randint(-5,5)
        birdie2.position.x = random.randint(-5,5)
        birdie2.position.y = random.randint(-5,5)
        birdie1.animate()
        birdie2.animate()
        turtle.update()
        delay(1)
        

    screen.exitonclick()
