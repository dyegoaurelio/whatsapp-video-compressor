import sys
from subprocess import run
from os import system, path
from math import ceil

MAX_BITS = 15.75 * 8000
filepath = sys.argv[-1]


def get_duration(path):
    return float(run(f'ffprobe -i {path} -show_entries format=duration -v quiet -of csv="p=0"', capture_output=True, shell=True).stdout)


file_size = path.getsize(filepath)
duration = get_duration(filepath)

bitrate = ceil(MAX_BITS / duration) - 128


filename = filepath.split('/')[-1]
file_extension = filename.split('.')[-1]
file_title = filename[:-len(file_extension) - 1]

system(f'ffmpeg -y -i {filepath} -c:v libx264 -b:v {bitrate}k -pass 1 -vsync cfr -f null /dev/null && \
ffmpeg -i {filepath} -c:v libx264 -b:v {bitrate}k -pass 2 -c:a aac -b:a 128k {file_title}-WHATSAPP.mp4')
