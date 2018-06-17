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
global width, rlines, gmode,  mode, i, shift, fline
width = 80
rlines = []
gmode = ''
mode = ''
i = [0, 0]
shift = ['']
last_a = ''
fline = ''
# formatting line


def cmd(lines):
    global width, rlines, gmode, mode, i, shift, fline
    while True:
        if not i[1] < len(lines[i[0]]):
            i[0] += 1
            i[1] = 0
            break
        elif lines[i[0]][i[1]] == 'l':
            mode = 'l'
            i[1] += 1
        elif lines[i[0]][i[1]] == 'c':
            mode = 'c'
            i[1] += 1
        elif lines[i[0]][i[1]] == 'r':
            mode = 'r'
            i[1] += 1
        elif lines[i[0]][i[1]] == ':':
            gmode = mode
            k = shift
            shift = ['']
            for j in range(len(k)):
                shift.append(k[j])
            i[1] += 1
        elif lines[i[0]][i[1]] == 'e':
            gmode = ''
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
        elif lines[i[0]][i[1]] == '.':
            rlines += [fline+'\n']
            fline = ''
            i[1] += 1
        elif lines[i[0]][i[1]] == '"':
            m = gmode
            if mode != '':
                m = mode
            s = ''
            for j in shift:
                s = j + s
            w = width - len(s)
            e = lines[i[0]][i[1]+1:]
            if m == '':
                while e != '':
                    e = s + e
                    if len(e) > width:
                        c = e.rfind(' ', 0, 80)
                    else:
                        c = len(e)
                    rlines += [e[:c]+'\n']
                    for k in range(len(shift)):
                        shift[k] = re.compile('[a-zA-Z0-9_)(-]').sub(' ', shift[k])
                    s = ''
                    for j in shift:
                        s = j + s
                    e = e[c+1:]
            else:
                if fline == '':
                    fline = s + ' '*w
                    for k in range(len(shift)):
                        shift[k] = re.compile('[a-zA-Z0-9_)(-]').sub(' ', shift[k])
                ml = len(e)
                if m == 'l':
                    mf = len(s)
                    me = len(s) + ml
                elif m == 'r':
                    mf = width - ml
                    me = width
                elif m == 'c':
                    mf = len(s) + (w-ml)//2
                    me = mf + ml
                if fline[mf:me] != ml * ' ':
                    print('WARN(', i, '): covering \'', fline[mf:me], '\' by \'', e, '\'', sep='')
                fline = fline[:mf] + e + fline[me:]
            i[1] = len(lines[i[0]])
            shift[0] = ''
            mode = ''
        else:
            print('WARN(', i, '): don\'t know command ', lines[i[0]][i[1]], ', skipping', sep='')
            i[1] += 1


def interpreter(lines):
    global width, rlines, gmode,  mode, i, shift
    while i[0] < len(lines):
        if i[0] > 26:
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
