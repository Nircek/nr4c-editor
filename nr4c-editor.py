#!/usr/bin/python
# -*- coding: UTF-8 -*-
# file from https://github.com/Nircek/nr4c-editor
# licensed under MIT license

# MIT License

# Copyright (c) 2018 Nircek

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys
import re
global width, rlines, mode, i, shift
width = 80
rlines = []
mode = ''
i = [0, 0]
shift = ['']



def cmd(lines):
    global width, rlines, mode, i, shift
    while True:
        if not i[1] < len(lines[i[0]]):
            i[0] += 1
            i[1] = 0
            break
        # elif lines[i[0]][i[1]] == 'l':
        # elif lines[i[0]][i[1]] == 'c':
        # elif lines[i[0]][i[1]] == 'r':
        elif lines[i[0]][i[1]] == ':':
            k = shift
            shift = ['']
            for j in range(len(k)):
                shift.append(k[j])
            i[1] += 1
        elif lines[i[0]][i[1]] == 'e':
            k = shift
            shift = []
            for j in range(1, len(k)):
                shift.append(k[j])
            i[1] += 1
            shift[0] = ''
        elif lines[i[0]][i[1]] == 'p':
            shift[0] += '   '
            i[1] += 1
        elif lines[i[0]][i[1]] == '-':
            shift[0] += ' - '
            i[1] += 1
        elif lines[i[0]][i[1]] == '"':
            s = ''
            for j in shift:
                s = j + s
            e = s + lines[i[0]][i[1]+1:]
            while len(e) > width:
                c = e.rfind(' ', 0, 80)
                rlines += [e[:c]+'\n']
                # delete a) - etc.
                e = re.compile('[a-zA-Z0-9_)(-]').sub(' ', s) + e[c+1:]
            rlines += [e]
            rlines[-1] += '\n'
            i[1] = len(lines[i[0]])
            shift[0] = ''
        else:
            print('WARN(', i, '): don\'t know command ', lines[i[0]][i[1]], ', skipping', sep='')
            i[1] += 1


def interpreter(lines):
    global width, rlines, mode, i, shift
    while i[0] < len(lines):
        if i[0] > 114:
            print(end='')
        if len(lines[i[0]]) == 0:
            rlines += ['\n']
            i[0] += 1
            continue
        if lines[i[0]][0] == '#':
            i[0] += 1
            continue
        elif lines[i[0]][0] == '/':
            i[1] = 1
            cmd(lines)
        else:
            rlines += lines[i[0]]
            i[0] += 1
    nrlines = []
    for line in rlines:
        nrlines += line + '\n'
    return rlines


if __name__ == '__main__':
    try:
        if len(sys.argv) > 1:
            fi = open(sys.argv[1], 'r')
        else:
            fi = open(input('INPUT FILE: '), 'r')
        if len(sys.argv) > 2:
            fo = open(sys.argv[2], 'w')
        else:
            fo = open(input('OUTPUT FILE: '), 'w')
        fo.writelines(interpreter(fi.read().splitlines()))
    except FileNotFoundError:
        print('This file cannot be found...', file=sys.stderr)
        if len(sys.argv) > 1:
            print('Usage: ', sys.argv[0], ' [INPUT FILE] [OUTPUT FILE]', file=sys.stderr)
    finally:
        if 'fi' in locals():
            fi.close()
        if 'fo' in locals():
            fo.close()
