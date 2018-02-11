from random import random


def bernoulli(p):
    '''Simulates a benoulli event given a probability'''
    x = random()
    if x >= p:
        return 0
    else:
        return 1
