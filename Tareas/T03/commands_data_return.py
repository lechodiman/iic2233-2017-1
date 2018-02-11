import my_csv
from my_types import to_filter, to_operation, float_range, is_iterable, is_number
from my_math import sqrt
import my_exceptions
from os.path import isfile


def get_column(file_name, column_name, o_instance):
    if not isinstance(file_name, str):
        raise my_exceptions.ErrorDeTipo()
    if not isinstance(column_name, str):
        raise my_exceptions.ErrorDeTipo()
    if not isfile(file_name + '.csv'):
        raise my_exceptions.ReferenciaInvalida()
    with open(file_name + '.csv') as f:
        reader = my_csv.reader(f, delimiter=';')
        header = next(reader)
        header_wo_types = [i.split(':')[0] for i in header]
        df = {header_wo_types[i]: i for i in range(len(header))}

        if column_name not in df:
            raise my_exceptions.ReferenciaInvalida()

        for row in reader:
            v = row[df[column_name]]
            if not is_number(v):
                if v in dir(o_instance):
                    v = getattr(o_instance, v)
                else:
                    raise my_exceptions.ReferenciaInvalida()
            yield float(v)


def filtrar(column, symbol, value, o_instance):
    if isinstance(column, str):
        if column in dir(o_instance):
            column = getattr(o_instance, column)
        else:
            raise my_exceptions.ReferenciaInvalida()
    if isinstance(value, str):
        if value in dir(o_instance):
            value = getattr(o_instance, value)
        else:
            raise my_exceptions.ReferenciaInvalida()
    if not is_iterable(column):
        raise my_exceptions.ImposibleProcesar()
    if not isinstance(symbol, str):
        raise my_exceptions.ErrorDeTipo()
    if not is_number(value):
        raise my_exceptions.ErrorDeTipo()

    for i in filter(to_filter(symbol, value), column):
        yield i


def operar(column, symbol, value, o_instance):
    if isinstance(column, str):
        if column in dir(o_instance):
            column = getattr(o_instance, column)
        else:
            raise my_exceptions.ReferenciaInvalida()
    if isinstance(value, str):
        if value in dir(o_instance):
            value = getattr(o_instance, value)
        else:
            raise my_exceptions.ReferenciaInvalida()
    if not is_iterable(column):
        raise my_exceptions.ImposibleProcesar()
    if not isinstance(symbol, str):
        raise my_exceptions.ErrorDeTipo()
    if not str(value).isnumeric():
        raise my_exceptions.ErrorDeTipo()

    for i in map(to_operation(symbol, value), column):
        yield i


def evaluar(function, start, end, step, o_instance):
    if isinstance(function, str):
        if function in dir(o_instance):
            function = getattr(o_instance, function)
        else:
            raise my_exceptions.ReferenciaInvalida()
    if type(function).__name__ != 'function':
        raise my_exceptions.ErrorDeTipo()
    for i in (function(x) for x in float_range(start, end, step)):
        yield i


def LEN(column, o_instance):
    if isinstance(column, str):
        if column in dir(o_instance):
            column = getattr(o_instance, column)
        else:
            raise my_exceptions.ReferenciaInvalida()
    if not is_iterable(column):
        raise my_exceptions.ErrorDeTipo()
    return len(list(column))


def PROM(column, o_instance):
    if isinstance(column, str):
        if column in dir(o_instance):
            column = getattr(o_instance, column)
        else:
            raise my_exceptions.ReferenciaInvalida()
    if not is_iterable(column):
        raise my_exceptions.ErrorDeTipo()
    enum = [(i, v) for i, v in enumerate(column)]
    n = len(enum)
    if n == 0:
        raise my_exceptions.ErrorMatematico()
    Sum = sum(j for i, j in enum)
    return Sum / n


def DESV(column, o_instance):
    if isinstance(column, str):
        if column in dir(o_instance):
            column = getattr(o_instance, column)
        else:
            raise my_exceptions.ReferenciaInvalida()
    if not is_iterable(column):
        raise my_exceptions.ErrorDeTipo()

    l_col = list(column)
    avg = PROM(l_col, o_instance)
    sigma = sqrt(sum((i - avg)**2 for i in l_col) / len(l_col))

    return sigma


def VAR(column, o_instance):
    return DESV(column, o_instance)**2


def MEDIAN(column, o_instance):
    if isinstance(column, str):
        if column in dir(o_instance):
            column = getattr(o_instance, column)
        else:
            raise my_exceptions.ReferenciaInvalida()
    if not is_iterable(column):
        raise my_exceptions.ErrorDeTipo()
    l_col = list(column)
    n = len(l_col)
    if n == 0:
        raise my_exceptions.ImposibleProcesar()
    if n % 2 == 0:
        m_1 = l_col[int(n / 2)]
        m_2 = l_col[int(n / 2 - 1)]
        return (m_1 + m_2) / 2
    else:
        m = l_col[int(n / 2)]
        return m


# Commands with boolean return

def apply_command(column, command, o_instance):
    available_commands = {'LEN': LEN, 'PROM': PROM, 'DESV': DESV,
                          'VAR': VAR, 'MEDIAN': MEDIAN}

    if command not in available_commands:
        raise my_exceptions.ArgumentoInvalido()
    else:
        return available_commands[command](column, o_instance)


def comparar_columna(column_1, symbol, command, column_2, o_instance):
    v_1 = apply_command(column_1, command, o_instance)
    v_2 = apply_command(column_2, command, o_instance)

    return to_filter(symbol, v_2)(v_1)


def comparar(num_1, symbol, num_2, o_instance):
    if isinstance(num_1, str):
        if num_1 in dir(o_instance):
            num_1 = getattr(o_instance, num_1)
        else:
            raise my_exceptions.ReferenciaInvalida()
    if isinstance(num_2, str):
        if num_2 in dir(o_instance):
            num_2 = getattr(o_instance, num_2)
        else:
            raise my_exceptions.ReferenciaInvalida()
    if not is_number(num_1):
        raise my_exceptions.ErrorDeTipo()
    if not is_number(num_2):
        raise my_exceptions.ErrorDeTipo()
    if not isinstance(symbol, str):
        raise my_exceptions.ErrorDeTipo()

    return to_filter(symbol, num_2)(num_1)
