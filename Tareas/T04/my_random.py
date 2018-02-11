from random import uniform


def weighted_choice(choices):
    '''Returns a random selection from the weighted choices
    choices : [(choice_1, weight_1), (choice_n, weight_n)]'''
    total = sum(w for c, w in choices)
    r = uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"
