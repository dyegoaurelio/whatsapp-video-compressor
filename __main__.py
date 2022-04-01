import sys
from subprocess import run
from os import system, path
from math import ceil
MAX_SIZE = 15.5 * 1024 * 1024
filename = sys.argv[-1]


# file_size = path.getsize(filename)

# proportion = ceil(file_size/MAX_SIZE)

proportion = 6


system(
    f'ffmpeg -i {filename} -vf "scale=trunc(iw/{proportion})*2:trunc(ih/{proportion})*2" ' \
        '-c:v libx264 -crf 28 -acodec aac -profile:v baseline -level 3.0 -pix_fmt yuv420p   output5.mp4'
)

# %%
# num = 17

# MAX_DIV = 5
# extra = num % MAX_DIV
# qtd_max = int((num - extra)/MAX_DIV)
# print(extra, qtd_max)
