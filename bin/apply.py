#!/usr/bin/env python

import os
import shlex
import sys

src_dir = sys.argv[1]
dst_dir = sys.argv[2]

proj_dir = os.path.dirname(sys.argv[0]) + '/..'
meta_dir = proj_dir + '/ffmeta'

for file in os.listdir(meta_dir):
    if not file.endswith('.txt'):
        break

    fn_src = file[:-4]
    if fn_src.endswith('.avi'):
        fn_dst = fn_src[:-4] + '.mp4'
    else:
        fn_dst = fn_src
    src_file = shlex.quote(src_dir + '/' + fn_src)
    dst_file = shlex.quote(dst_dir + '/' + fn_dst)
    meta_file = shlex.quote(meta_dir + '/' + file)
    cmd = f'ffmpeg -y -i {src_file} -i {meta_file} -map_metadata 1 -codec copy {dst_file}'

    print(f'>>> {cmd}')
    os.system(cmd)
