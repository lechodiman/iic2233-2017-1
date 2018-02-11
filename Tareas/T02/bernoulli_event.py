from random import random, randrange


def bernoulli(p):
    '''Simulates a benoulli event given a probability'''
    x = random()
    if x >= p:
        return 0
    else:
        return 1


def uniform(a=0, b=6):
    x = randrange(a, b + 1)
    return x


if __name__ == "__main__":

    p = 0.62
    print(sum(bernoulli(p) for i in range(1000)) / 1000)
    # print(sum(uniform(0, 10) for i in range(100000)) / 100000)
