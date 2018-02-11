def sqrt(x):
    '''
    Returns the square root of x
    '''
    return x**(1 / 2)


def factorial(x):
    '''Find x!'''
    if x < 0:
        raise ValueError
    else:
        if x == 0 or x == 1:
            return 1
        else:
            return factorial(x - 1) * x
