#!/usr/bin/env python3

import sys
from subprocess import run
from os import system, path, rename, remove
from math import floor

MAX_BITS = 15.6 * 8000
MAX_SIZE = 16e+6
AUDIO_BITRATE = 128


def get_duration(path):
    return float(run(f'ffprobe -i {path} -show_entries format=duration -v quiet -of csv="p=0"', capture_output=True, shell=True).stdout)


def compress_video(in_path, out_path, bitrate_factor=1):
    duration = get_duration(in_path)

    bitrate = (floor(MAX_BITS / duration) - AUDIO_BITRATE) * bitrate_factor

    system(f'ffmpeg -hwaccel cuda -y -i {in_path} -c:v libx264 -b:v {bitrate}k -pass 1 -vsync cfr -f null /dev/null && \
    ffmpeg -hwaccel cuda -i {in_path} -c:v libx264 -b:v {bitrate}k \
        -pass 2 -c:a aac -b:a {AUDIO_BITRATE}k {out_path}')

    folder = path.dirname(path.realpath(in_path))

    system(f'rm {folder}/ffmpeg2pass-0.log*')


def main():

    filepath = sys.argv[-1]

    if len(sys.argv) == 1:
        raise ValueError('insira o caminho do vídeo')

    filename = filepath.split('/')[-1]
    file_extension = filename.split('.')[-1]
    file_title = filename[:-len(file_extension) - 1]

    should_compress = True

    out_path = f'{file_title}-WHATSAPP.mp4'
    in_path = filepath

    bitrate_factor = float(1)
    temp_in_path = None

    while should_compress:
        compress_video(in_path, out_path, bitrate_factor)

        if temp_in_path:
            remove(temp_in_path)

        out_size = path.getsize(out_path)

        if out_size > MAX_SIZE:
            print(
                f'\n------------------\n'
                f'Tamanho maior do que {MAX_SIZE*1e-6:.2f} mb ({out_size*1e-6:.2f} mb)'
                'recomprimindo ...'
                '\n------------------\n'
            )
            bitrate_factor = bitrate_factor * 0.8
            temp_in_path = out_path + '.temp'
            rename(out_path, temp_in_path)

            in_path = temp_in_path

        else:
            should_compress = False


if __name__ == '__main__':
    main()
