#!/usr/bin/env python

# adapted from https://ikyle.me/blog/2020/add-mp4-chapters-ffmpeg

import os
import sys
import re


def process_file(src, dst):
    chapters = list()

    with open(src, 'r') as f:
        for line in f:
            if line.startswith(';') or line == '\n':
                continue

            x = re.match(r'(\d{1,2}):(\d{1,2}):(\d{1,2}).(\d{3}) (.*)', line)
            if x is None:
                print(f'Skipping line: {line}', end='')
                continue

            h = int(x.group(1))
            m = int(x.group(2))
            s = int(x.group(3))
            ms = int(x.group(4))
            title = x.group(5)

            ts = ((h * 60 + m) * 60 + s) * 1000 + ms
            chapters.append({
                'title': title,
                'ts': ts,
            })

    result = ';FFMETADATA1\n'

    for i in range(len(chapters) - 1):
        chap = chapters[i]
        title = chap['title']
        start = chap['ts']
        end = chapters[i + 1]['ts'] - 1
        result += f"""
[CHAPTER]
TIMEBASE=1/1000
START={start}
END={end}
title={title}
"""

    with open(dst, 'w') as myfile:
        myfile.write(result)


proj_dir = os.path.dirname(sys.argv[0]) + '/..'
src_dir = proj_dir + '/src'
meta_dir = proj_dir + '/ffmeta'

for file in os.listdir(src_dir):
    if not file.endswith('.txt'):
        break

    process_file(src_dir + '/' + file, meta_dir + '/' + file)
