from datetime import datetime


def is_prime(a):
    return all(a % i for i in range(2, a))


def is_malvado(a):
    return bin(a).count('1') % 2 == 0


def gen_prime_():
    i = 2
    while True:
        if is_prime(i):
            yield i
        i += 1


def gen_malvado_():
    i = 1
    while True:
        if is_malvado(i):
            yield i
        i += 1

gen_malvado = gen_malvado_()
gen_prime = gen_prime_()

with open('chatayudantes.iic2233', 'rb') as file:
    bytes_file = bytearray(file.read())
    i = 0
    bytes_list = []
    bytes_sum = []

    '''
    lala = []
    for i, b in enumerate(bytes_file):
        lala.append(b)
        if i == 40:
            break
    '''

    print()
    lista_corrigiendo = []
    for b in bytes_file:
        lista_corrigiendo.append(b)
        if len(lista_corrigiendo) == 4:
            bytes_sum.append(sum(lista_corrigiendo))
            lista_corrigiendo = []

    print(bytes_sum[0:40])
    print()

bytes_replaced = []
for num in bytes_sum:
    num_str = str(num)
    if len(num_str) != 3:
        num_str = num_str.zfill(3)

    new_num_str = ''

    for digit in num_str:
        if digit == '1':
            digit = '9'
        elif digit == '9':
            digit = '1'

        elif digit == '2':
            digit = '8'
        elif digit == '8':
            digit = '2'

        elif digit == '3':
            digit = '7'
        elif digit == '7':
            digit = '3'

        elif digit == '4':
            digit = '6'
        elif digit == '6':
            digit = '4'

        elif digit == '0':
            digit = '5'
        elif digit == '5':
            digit = '0'

        new_num_str += digit

    new_num_str = new_num_str[::-1]
    # new_num_str.zfill(3)

    bytes_replaced.append(new_num_str)

print(bytes_replaced[0:40])

# Paso 2

bytes_wav = []
bytes_gif = []

contador = 0
i = 0
while i < len(bytes_replaced):
    if contador % 2 == 0:
        chunk_len = next(gen_prime)
        if len(bytes_wav) == 9783:
            print('empece a hacer el gif')
            bytes_gif.extend(bytes_replaced[i: len(bytes_replaced)])
            break

        elif len(bytes_wav) + chunk_len > 9783:
            chunk_len = 9783 - len(bytes_wav)
        bytes_wav.extend(bytes_replaced[i: i + chunk_len])
        i = i + chunk_len

    else:
        chunk_len = next(gen_malvado)
        bytes_gif.extend(bytes_replaced[i: i + chunk_len])
        i = i + chunk_len

    contador += 1

b_array_wav = bytearray([int(i) for i in bytes_wav])
b_array_gif = bytearray([int(i) for i in bytes_gif])


start = datetime.now()
with open('audio.wav', 'wb') as file:
    contador = 0
    while contador < len(b_array_wav):
        if contador + 512 < len(b_array_wav):
            print('TOTAL : {}, PROCESADO: {}, SIN PROCESAR: {}, DELTA TIME: {}'.format(len(b_array_wav),
                                                                                       contador, len(b_array_wav) - contador,
                                                                                       datetime.now() - start))
            file.write(b_array_wav[contador: contador + 512])
        else:
            file.write(b_array_wav[contador: len(b_array_wav)])
            break
        contador += 512

with open('imagen.gif', 'wb') as file:
    contador = 0
    while contador < len(b_array_gif):
        if contador + 1024 < len(b_array_gif):
            print('TOTAL : {}, PROCESADO: {}, SIN PROCESAR: {}, DELTA TIME: {}'.format(len(b_array_gif),
                                                                                       contador, len(b_array_gif) - contador,
                                                                                       datetime.now() - start))

            file.write(b_array_gif[contador: contador + 1024])
        else:
            file.write(b_array_gif[contador: len(b_array_gif)])
            break
        contador += 1024
