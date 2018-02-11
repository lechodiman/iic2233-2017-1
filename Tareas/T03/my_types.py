import my_exceptions


def is_iterable(thing):
    if isinstance(thing, str):
        return False
    try:
        iter(thing)
    except TypeError:
        return False
    return True


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def float_range(x, y, step=1.0):
    if is_number(x):
        x = float(x)
    if is_number(y):
        y = float(y)
    if is_number(step):
        step = float(step)
    if x < y:
        if step <= 0:
            raise my_exceptions.ImposibleProcesar()
        while x < y:
            yield float(x)
            x += step
    elif x > y:
        if step >= 0:
            raise my_exceptions.ImposibleProcesar()
        while y < x:
            yield float(x)
            x += step


def to_range(range_str):
    params = range_str.split(':')[1].split(',')
    a = int(params[0])
    b = int(params[1])
    c = 1 if len(params) < 3 else int(params[2])

    return float_range(a, b, c)


def to_filter(symbol, value):
    value = float(value)
    available_symbols = ['==', '>', '<', '>=', '<=', '!=']
    if symbol not in available_symbols:
        raise my_exceptions.ErrorDeTipo()
    else:
        if symbol == '==':
            return lambda x: x == value
        elif symbol == '>':
            return lambda x: x > value
        elif symbol == '<':
            return lambda x: x < value
        elif symbol == '>=':
            return lambda x: x >= value
        elif symbol == '<=':
            return lambda x: x <= value
        elif symbol == '!=':
            return lambda x: x != value


def to_operation(symbol, value):
    value = float(value)
    available_symbols = ['*', '/', '+', '-', '>=<']
    if symbol not in available_symbols:
        raise my_exceptions.ErrorDeTipo()
    else:
        if symbol == '*':
            return lambda x: x * value
        elif symbol == '/':
            return lambda x: x / value
        elif symbol == '+':
            return lambda x: x + value
        elif symbol == '-':
            return lambda x: x - value
        elif symbol == '>=<':
            return lambda x: round(x, value)
