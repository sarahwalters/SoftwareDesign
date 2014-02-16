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
    
    if max_depth == 2:
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
    red = build_random_function(10, 15)
    green = build_random_function(10, 15)
    blue = build_random_function(10, 15)
    
    im = Image.new("RGB",(x_size, y_size))
    pixels = im.load()
    
    for i in range(x_size):
        for j in range(y_size):
            x = scale_down(i)
            y = scale_down(j)
            
            r = scale_up(evaluate_random_function(red, x, y))
            g = scale_up(evaluate_random_function(green, x, y))
            b = scale_up(evaluate_random_function(blue, x, y))
            pixels[i, j] = (r, g, b)
            
    im.save(filename)
    print "shown"
            
            
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