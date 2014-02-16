# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 11:34:57 2014

@author: pruvolo
"""

# you do not have to use these particular modules, but they may help
from random import randint
from math import sin
from math import cos
from math import pi
from math import floor
import Image

def build_random_function(min_depth, max_depth):
    """ Recursively constructs a function composed of simpler functions
    
        Inputs: min_depth and max_depth describe how many layers of recursion occur 
            -> sin(sin(x)) has a depth of 2, for instance.
        Output: nested-list representation of the function, for use with evaluate_random_function.
    """
    
    if max_depth == 1:
        no_args = [["x"], ["y"]]
        a = no_args[randint(0,1)]
        b = no_args[randint(0,1)]
    else:
        a = build_random_function(min_depth-1, max_depth-1)
        b = build_random_function(min_depth-1, max_depth-1)
        
    f = [["prod", a, b], 
         ["cos_pi", a],
         ["sin_pi", a],
         ["x"],
         ["y"]]
    
    if min_depth > 1:
        i = randint(0, 2)
    else:
        i = randint(0, 4)
    return f[i]
    

def build_random_lambda(min_depth, max_depth):
    prod = lambda a,b: a*b
    sin_pi = lambda a,b: sin(pi*a)
    cos_pi = lambda a,b: cos(pi*a)
    x = lambda a,b: a
    y = lambda a,b: b
    
    f = [prod, sin_pi, cos_pi, x, y]
    
    if max_depth == 1:
        i = randint(3,4)
        return lambda a,b: f[i](a,b)
    else:
        if min_depth > 1:
            i = randint(0,2)
        else:
            i = randint(0,4)
        g = build_random_lambda(min_depth-1, max_depth-1)
        h = build_random_lambda(min_depth-1, max_depth-1)
        return lambda a,b: f[i](g(a,b),h(a,b))


def evaluate_random_function(f, x, y):
    # your doc string goes here
    if f[0] == "x":
        return x
    elif f[0] == "y":
        return y
    elif f[0] == "sin_pi":
        return sin(pi*evaluate_random_function(f[1], x, y))
    elif f[0] == "cos_pi":
        return cos(pi*evaluate_random_function(f[1], x, y))
    elif f[0] == "prod":
        return evaluate_random_function(f[1], x, y) * evaluate_random_function(f[2], x, y)
        

def draw_image(x_size, y_size, filename):
    # using nested lists
    red = build_random_function(10, 12)
    green = build_random_function(5, 7)
    blue = build_random_function(7, 9)
    
    # using lambdas
    #red = build_random_lambda(10,12)
    #green = build_random_lambda(5,7)
    #blue = build_random_lambda(7,9)
    
    im = Image.new("RGB",(x_size, y_size))
    pixels = im.load()
    
    for i in range(x_size):
        for j in range(y_size):
            x = scale_down(i)
            y = scale_down(j)
            
            # using nested lists
            r = scale_up(evaluate_random_function(red, x, y))
            g = scale_up(evaluate_random_function(green, x, y))
            b = scale_up(evaluate_random_function(blue, x, y))
            
            # using lambdas
            #r = scale_up(red(x,y))
            #g = scale_up(green(x,y))
            #b = scale_up(blue(x,y))
            pixels[i, j] = (r, g, b)
            
    im.save(filename)
    print "done"
            
            
def scale_down(x):
    """ converts from range [0,255] to range [-1,1]
        input: number to convert
        output: conversion
    """
    return (2*x/255.0)-1

def scale_up(x):
    """ converts from range [-1,1] to range [0,255]
        input: number to convert
        output: conversion
    """
    return int((x+1)*255.0/2)