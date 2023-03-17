#!/usr/bin/env python

import os
import shlex
import sys


def process(src_dir, dst_dir, meta_dir):
    for file in os.listdir(meta_dir):
        meta_path = meta_dir + '/' + file

        if os.path.isdir(meta_path):
            process(src_dir + '/' + file, dst_dir + '/' + file, meta_path)
            continue

        if not file.endswith('.txt'):
            continue

        params = ''

        fn_src = file[:-4]
        if fn_src == 'AMV Hell 3 - The Motion Picture.avi':
            # fix desync problem in AMV Hell 3
            params += '-fflags +genpts '
        if fn_src.endswith('.avi'):
            fn_dst = fn_src[:-4] + '.mkv'
        else:
            fn_dst = fn_src
        src_file = src_dir + '/' + fn_src
        src_file_q = shlex.quote(src_dir + '/' + fn_src)
        dst_file_q = shlex.quote(dst_dir + '/' + fn_dst)
        meta_file_q = shlex.quote(meta_path)

        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir, exist_ok=True)

        if not os.path.exists(src_file):
            print(f'Skipping missing {fn_src}')
            continue

        cmd = f'ffmpeg {params} -i {src_file_q} -i {meta_file_q} -map_metadata 1 -codec copy {dst_file_q}'

        print(f'>>> {cmd}')
        os.system(cmd)


src_dir = sys.argv[1]
dst_dir = sys.argv[2]

proj_dir = os.path.dirname(sys.argv[0]) + '/..'
meta_dir = proj_dir + '/ffmeta'

process(src_dir, dst_dir, meta_dir)
