from math import e, pi
from my_math import factorial, sqrt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from my_types import to_range, is_number, is_iterable
import my_exceptions

style.use('ggplot')


def normal(*args):
    if len(args) != 3:
        raise my_exceptions.ArgumentoInvalido()
    mu = args[0]
    sigma = args[1]
    o_instance = args[2]

    if isinstance(mu, str):
        if mu in dir(o_instance):
            mu = getattr(o_instance, mu)
        else:
            raise my_exceptions.ReferenciaInvalida()
    if isinstance(sigma, str):
        if sigma in dir(o_instance):
            sigma = getattr(o_instance, sigma)
        else:
            raise my_exceptions.ReferenciaInvalida()

    if False in [is_number(arg) for arg in args[0:-1]]:
        raise my_exceptions.ErrorDeTipo()

    def normal_x(x, mu=mu, sigma=sigma):
        if not is_number(x):
            raise my_exceptions.ErrorDeTipo()
        if sigma == 0:
            raise my_exceptions.ErrorMatematico()
        f_x = (1 / sqrt(2 * pi * sigma**2)) * e**((-1 / 2) * ((x - mu) / sigma)**2)
        return f_x
    return normal_x


def gamma(*args):
    if len(args) != 3:
        raise my_exceptions.ArgumentoInvalido()
    k = args[0]
    nu = args[1]
    o_instance = args[2]

    if isinstance(k, str):
        if k in dir(o_instance):
            k = getattr(o_instance, k)
        else:
            raise my_exceptions.ReferenciaInvalida()
    if isinstance(nu, str):
        if nu in dir(o_instance):
            nu = getattr(o_instance, nu)
        else:
            raise my_exceptions.ReferenciaInvalida()

    if False in [is_number(arg) for arg in args[0:-1]]:
        raise my_exceptions.ErrorDeTipo()

    def gamma_x(x, k=k, nu=nu):
        if x < 0:
            raise my_exceptions.ErrorMatematico()
        else:
            if k < 1.0:
                raise my_exceptions.ErrorMatematico()
            if type(k) != int:
                raise my_exceptions.ImposibleProcesar()
            f_x = nu**k * x**(k - 1) * e**(-nu * x) / factorial(k - 1)
            return f_x
    return gamma_x


def exponential(*args):
    if len(args) != 2:
        raise my_exceptions.ArgumentoInvalido()
    nu = args[0]
    o_instance = args[1]

    if isinstance(nu, str):
        if nu in dir(o_instance):
            nu = getattr(o_instance, nu)
        else:
            raise my_exceptions.ReferenciaInvalida()

    if False in [is_number(arg) for arg in args[0:-1]]:
        raise my_exceptions.ErrorDeTipo()

    def exponential_x(x, nu=nu):
        if x < 0:
            raise my_exceptions.ErrorMatematico()
        else:
            f_x = nu * e**(-nu * x)
            return f_x
    return exponential_x


def generate_distribution(model_name, *args):
    available_models = {'NORMAL': normal, 'GAMMA': gamma, 'EXPONENTIAL': exponential}
    if model_name in available_models:
        function = available_models[model_name](*args)
        return function
    else:
        raise my_exceptions.ErrorDeTipo()


def graficar(column, option, o_instance):
    if isinstance(column, str):
        if column in dir(o_instance):
            column = getattr(o_instance, column)
        else:
            raise my_exceptions.ReferenciaInvalida()
    if not is_iterable(column):
        raise my_exceptions.ImposibleProcesar()
    if not isinstance(option, str):
        raise my_exceptions.ImposibleProcesar()

    available_options = ['numerico', 'normalizado']
    y = np.array(list(column))

    if len(y) == 0:
        raise my_exceptions.ErrorDeTipo()

    if option in available_options:
        if option == 'numerico':
            x = np.array([i for i in range(0, len(y))])
        elif option == 'normalizado':
            suma = sum(y)
            x = np.array([i for i in range(0, len(y))]) / suma
    elif 'rango' in option:
        my_range = to_range(option)
        x = np.array([i for i in my_range])
        if len(x) != len(y):
            raise my_exceptions.ImposibleProcesar()
    elif isinstance(option, str):
        if option in dir(o_instance):
            option = getattr(o_instance, option)
            if is_iterable(option):
                x = np.array(list(option))
                if len(x) != len(y):
                    raise my_exceptions.ImposibleProcesar()
            else:
                raise my_exceptions.ImposibleProcesar()
    elif is_iterable(option):
        x = np.array(list(option))
        if len(x) != len(y):
            raise my_exceptions.ImposibleProcesar()
    else:
        raise my_exceptions.ImposibleProcesar()

    plt.plot(x, y)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

    return 'Graficando'
