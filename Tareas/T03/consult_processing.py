from basic_commands import generate_distribution, graficar
from commands_data_return import get_column, filtrar, operar, evaluar,\
    LEN, PROM, DESV, VAR, MEDIAN, comparar_columna, comparar
import my_exceptions

available_functions = {'crear_funcion': generate_distribution,
                       'graficar': graficar, 'extraer_columna': get_column, 'filtrar': filtrar,
                       'operar': operar, 'evaluar': evaluar, 'LEN': LEN, 'PROM': PROM,
                       'DESV': DESV, 'MEDIAN': MEDIAN, 'VAR': VAR, 'comparar_columna': comparar_columna,
                       'comparar': comparar}


def asignar(var, value, o_instance):
    if var not in (list(available_functions.keys()) + ['asignar']):
        setattr(o_instance, var, value)
        return 'asignar'
    else:
        raise my_exceptions.ImposibleProcesar()


available_functions['asignar'] = asignar


def unit_process_consult(consult, o_instance):
    consult_types = [type(o) for o in consult]
    if list not in consult_types:
        args = consult[1:]
        args.append(o_instance)
        return available_functions[consult[0]](*args)
    else:
        args = [unit_process_consult(i, o_instance) if type(i) is list else i for i in consult[1:]]
        args.append(o_instance)
        return available_functions[consult[0]](*args)


class A:
    pass


a = A()
