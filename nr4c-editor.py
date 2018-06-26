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
import copy
import datetime
g = {}
g['width'] = 80
g['rlines'] = []
g['gmode'] = ''
g['mode'] = ''
g['i'] = [0, 0]
g['shift'] = ['']
g['last_a'] = [chr(ord('a')-1)]
g['fline'] = ''
g['roz'] = 0
g['pod'] = 0
# formatting line
g['v'] = {'D': datetime.date.today().strftime('%#d %B %Y'), 'd': datetime.date.today().strftime('%Y-%m-%d')}
g['indent'] = ''
g['indented'] = False
# int = inteligent
g['intfirst'] = ()
g['intmax'] = 0
g['intsec'] = False


def find(st, s):
    i = 0
    if len(s) >= 2:
        if s[0] == s[1]:
            raise ValueError('this is not possible to find string with double first character')
    while True:
        i = st.find(s, i)
        if i == -1:
            return i
        if st[i-1] == s[0]:
            continue
        if st[i+1] == s[0]:
            i += 2
            continue
        return i


def cmd(lines):
    global g
    while True:
        if not g['i'][1] < len(lines[g['i'][0]]):
            g['i'][0] += 1
            g['i'][1] = 0
            g['indented'] = False
            break
        elif lines[g['i'][0]][g['i'][1]] == 'l':
            g['mode'] = 'l'
            g['i'][1] += 1
        elif lines[g['i'][0]][g['i'][1]] == 'c':
            g['mode'] = 'c'
            g['i'][1] += 1
        elif lines[g['i'][0]][g['i'][1]] == 'r':
            g['mode'] = 'r'
            g['i'][1] += 1
        elif lines[g['i'][0]][g['i'][1]] == ':':
            g['gmode'] = g['mode']
            g['shift'].insert(0, '')
            g['last_a'].insert(0, chr(ord('a')-1))
            g['i'][1] += 1
        elif lines[g['i'][0]][g['i'][1]] == 'e':
            g['gmode'] = ''
            g['last_a'].pop(0)
            g['shift'].pop(0)
            g['i'][1] += 1
            g['shift'][0] = ''
        elif lines[g['i'][0]][g['i'][1]] == 'p':
            g['shift'][0] += '   '
            g['i'][1] += 1
        elif lines[g['i'][0]][g['i'][1]] == 's':
            g['i'][1] += 1
            g['roz'] += 1
            g['pod'] = 0
            g['shift'][0] += str(g['roz']) + ' '
        elif lines[g['i'][0]][g['i'][1]] == 'u':
            g['i'][1] += 1
            g['pod'] += 1
            g['shift'][0] += str(g['roz']) + '.' + str(g['pod']) + ' '
        elif lines[g['i'][0]][g['i'][1]] == 'a':
            g['last_a'][0] = chr(ord(g['last_a'][0])+1)
            g['shift'][0] += g['last_a'][0]+') '
            g['i'][1] += 1
        elif lines[g['i'][0]][g['i'][1]] == '-':
            g['shift'][0] += ' - '
            g['i'][1] += 1
        elif lines[g['i'][0]][g['i'][1]] == '/':
            g['indented'] = True
            g['i'][1] += 1
        elif lines[g['i'][0]][g['i'][1]] == '\\':
            if g['intsec']:
                g['intmax'] = 0
                g['intfirst'] = ()
                g['i'][1] += 1
            else:
                intsec = g['intsec']
                intmax = g['intmax']
                g = g['intfirst']
                # g['i'][1] = 1
                g['intsec'] = intsec
                g['intmax'] = intmax
            g['intsec'] = not g['intsec']
        elif lines[g['i'][0]][g['i'][1]] == '.':
            g['rlines'] += [g['fline']+'\n']
            g['fline'] = ''
            g['i'][1] += 1
        elif lines[g['i'][0]][g['i'][1]] == '%':
            e = lines[g['i'][0]][g['i'][1]+1:]
            if e.find('\"') == -1:
                g['i'][1] += 3
                g['v'][e[0]] = e[1]
            else:
                g['i'][1] += 1+len(e)
                g['v'][e[:e.find('\"')]] = e[e.find('\"')+1:]
        elif lines[g['i'][0]][g['i'][1]] == '"':
            m = g['gmode']
            if g['mode'] != '':
                m = g['mode']
            s = ''
            for j in g['shift']:
                s = j + s
            w = g['width'] - len(s)
            e = lines[g['i'][0]][g['i'][1]+1:]
            # changing vars to values
            for elem in g['v'].items():
                while True:
                    f = find(e, '%'+elem[0])
                    if f == -1:
                        break
                    e = e[:f] + elem[1] + e[f+len(elem[0])+1:]
            e = e.replace('%%', '%')
            if m == '':
                while e != '':
                    if g['indented']:
                        s = g['indent']
                    e = s + e
                    if len(e) > g['width']:
                        c = e.rfind(' ', 0, 80)
                    else:
                        c = len(e)
                    inteligent = find(e, '\\')
                    if inteligent != -1 and g['intfirst'] == () and not g['intsec']:
                        g['intfirst'] = copy.deepcopy(g)
                    g['rlines'] += [e[:c]+'\n']
                    f = find(g['rlines'][-1], '|')
                    g['rlines'][-1] = g['rlines'][-1].replace('||', '|')
                    if f != -1:
                        g['indent'] = ' '*f
                        g['rlines'][-1] = g['rlines'][-1][:f] + g['rlines'][-1][f+1:]
                        g['indented'] = True
                    for k in range(len(g['shift'])):
                        g['shift'][k] = len(g['shift'][k])*' '
                    s = ''
                    for j in g['shift']:
                        s = j + s
                    e = e[c+1:]
                    inteligent = find(g['rlines'][-1], '\\')
                    if inteligent != -1:
                        if g['intsec']:
                            # ----------
                            ee = g['rlines'][-1][:inteligent]+(g['intmax']-len(g['rlines'][-1][:inteligent]))*' '+g['rlines'][-1][inteligent+1:]
                            ee = ee.replace('\n', '')
                            del g['rlines'][-1]
                            while True:
                                if len(ee) > g['width']:
                                    c = ee.rfind(' ', 0, 80)
                                else:
                                    c = len(ee)
                                g['rlines'] += [ee[:c] + '\n']
                                if e == '':
                                    break
                                ee = g['intmax']*' ' + ee
                            # ----------
                        else:
                            g['intmax'] = max(g['intmax'], inteligent)
            else:
                if g['fline'] == '':
                    g['fline'] = s + ' '*w
                    for k in range(len(g['shift'])):
                        g['shift'][k] = len(g['shift'][k])*' '
                ml = len(e)
                if m == 'l':
                    mf = len(s)
                    me = len(s) + ml
                elif m == 'r':
                    mf = g['width'] - ml
                    me = g['width']
                elif m == 'c':
                    mf = len(s) + (w-ml)//2
                    me = mf + ml
                if g['fline'][mf:me] != ml * ' ':
                    print('WARN(', g['i'], '): covering \'', g['fline'][mf:me], '\' by \'', e, '\'', sep='')
                g['fline'] = g['fline'][:mf] + e + g['fline'][me:]
            g['i'][1] = len(lines[g['i'][0]])
            g['shift'][0] = ''
            g['mode'] = ''
        else:
            print('WARN(', g['i'], '): don\'t know command ', lines[g['i'][0]][g['i'][1]], ', skipping', sep='')
            g['i'][1] += 1


def interpreter(lines):
    global g
    while g['i'][0] < len(lines):
        if g['i'][0] > 27:
            print(end='')
        if len(lines[g['i'][0]]) == 0:
            g['rlines'] += ['\n']
            g['i'][0] += 1
            continue
        if lines[g['i'][0]][0] == '#':
            g['i'][0] += 1
            continue
        elif lines[g['i'][0]][0] == '/':
            g['i'][1] = 1
            cmd(lines)
        else:
            g['rlines'] += [lines[g['i'][0]]+'\n']
            g['i'][0] += 1
    return g['rlines']


if __name__ == '__main__':
    try:
        if len(sys.argv) > 1:
            fi = open(sys.argv[1], 'r', encoding='utf-8')
        else:
            fi = open(input('INPUT FILE: '), 'r', encoding='utf-8')
        if len(sys.argv) > 2:
            fo = open(sys.argv[2], 'w', encoding='utf-8')
        else:
            fo = open(input('OUTPUT FILE: '), 'w', encoding='utf-8')
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
