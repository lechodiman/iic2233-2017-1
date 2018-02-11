
def double_speed(path):
    '''It creates a new file, with 2x given a wav file(path) '''
    with open(path, 'rb') as file:
        chunk_id = file.read(4)
        print('Chunk id: {}'.format(chunk_id.decode('ascii')))

        chunk_size = file.read(4)
        print('Chunk size: {}'.format(int.from_bytes(chunk_size, byteorder='little')))

        Format = file.read(4)
        print('Format: {}'.format(Format.decode('ascii')))

        subchunk1_id = file.read(4)
        print('Subchunk1 ID: {}'.format(subchunk1_id.decode('ascii')))

        subchunk_size = file.read(4)
        print('Subchunk size : {}'.format(int.from_bytes(subchunk_size, byteorder='little')))

        audio_format = file.read(2)
        print('audio format: {}'.format(int.from_bytes(audio_format, byteorder='little')))

        num_channels = file.read(2)
        print('num channels: {}'.format(int.from_bytes(num_channels, byteorder='little')))

        sample_rate = file.read(4)
        print('sample_rate: {}'.format(int.from_bytes(sample_rate, byteorder='little')))

        byte_rate = file.read(4)
        print('byte_rate: {}'.format(int.from_bytes(byte_rate, byteorder='little')))

        block_align = file.read(2)
        print('block align: {}'.format(int.from_bytes(block_align, byteorder='little')))

        bytes_per_sample = file.read(2)
        print('bytes per sample: {}'.format(int.from_bytes(bytes_per_sample, byteorder='little')))

        subchunk2_id = file.read(4)
        print('subchunk2 id: {}'.format(subchunk2_id.decode('ascii')))

        subchunk2_size = file.read(4)
        print('sub chunk 2 size: {}'.format(int.from_bytes(subchunk2_size, byteorder='little')))

        data = file.read()

    # writes new file
    filename_out = path.replace('.wav', '')
    with open('{}_2x.wav'.format(filename_out), 'wb') as outfile:
        new_sample_rate = int.from_bytes(sample_rate, byteorder='little') * 2
        new_sample_rate = new_sample_rate.to_bytes(4, byteorder='little')

        new_byte_rate = int.from_bytes(byte_rate, byteorder='little') * 2
        new_byte_rate = new_byte_rate.to_bytes(4, byteorder='little')

        outfile.write(chunk_id)
        outfile.write(chunk_size)
        outfile.write(Format)
        outfile.write(subchunk1_id)
        outfile.write(subchunk_size)
        outfile.write(audio_format)
        outfile.write(num_channels)
        outfile.write(new_sample_rate)
        outfile.write(new_byte_rate)
        outfile.write(block_align)
        outfile.write(bytes_per_sample)
        outfile.write(subchunk2_id)
        outfile.write(subchunk2_size)
        outfile.write(data)

        print('File done')


if __name__ == '__main__':
    path = './Canciones/Pop/Justin Bieber - Sorry.wav'
    double_speed(path)
