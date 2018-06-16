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
width = 80


def cmd(lines, i, shift='', noend=False):
    rlines = []
    f = False
    while not f:
        if not i[1] < len(lines[i[0]]):
            i[0] += 1
            i[1] = 0
            break
        if lines[i[0]][i[1]] == 'p':
            shift += '   '
            i[1] += 1
        elif lines[i[0]][i[1]] == '"':
            e = shift + lines[i[0]][i[1]+1:]
            while len(e) > width:
                c = e.rfind(' ', 0, 80)
                rlines += [e[:c]+'\n']
                e = shift + e[c+1:]
                if noend:
                    print('WARN(', i, '): reach end of width', sep='')
            rlines += [e]
            if not noend:
                rlines[-1] += '\n'
            i[1] = len(lines[i[0]])
        else:
            print('WARN(', i, '): don\'t know command ', lines[i[0]][i[1]], ', skipping', sep='')
            i[1] += 1
    return [rlines, i]


def interpreter(lines):
    rlines = []
    i = [0, 0]
    while i[0] < len(lines):
        if i[0] == 26:
            print(end='')
        if len(lines[i[0]]) == 0:
            rlines += ['\n']
            i[0] += 1
        if lines[i[0]][0] == '#':
            i[0] += 1
            continue
        elif lines[i[0]][0] == '/':
            i[1] = 1
            r = cmd(lines, i)
            rlines += r[0]
            i = r[1]
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
