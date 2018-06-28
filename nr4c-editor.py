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


def greset():
    global g
    g = {
        'lines': [],
        'width': 80,
        'rlines': [],
        'gmode': '',
        'mode': '',
        'i': [0, 0],
        'shift': [''],
        'last_a': [chr(ord('a')-1)],
        'fline': '',
        'roz': 0,
        'pod': 0,
        'v': {'D': datetime.date.today().strftime('%#d %B %Y'), 'd': datetime.date.today().strftime('%Y-%m-%d'), 'p': '0'},
        'indent': '',
        'indented': False,
        'intfirst': (),
        'intmax': 0,
        'intsec': False,
        'didasmode': False,
        'didasindent': 0,
        'didasonly': False,
        'stop': False,
        'out': 'rlines',
        'iheader': None,
        'header': [],
        'ifooter': None,
        'footer': [],
        'split': False,
        'pages': [],
        'sections': [],
        'sectiontitle': False,
        'sectionreg': 2
        # 2 = collecting names
        # 1 = collecting pages
        # 0 = no collecting
    }


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


def cmd():
    global g
    while True:
        if not g['i'][1] < len(g['lines'][g['i'][0]]):
            g['i'][0] += 1
            g['i'][1] = 0
            g['indented'] = False
            if g['didasmode']:
                if g['didasindent'] == 0:
                    g['out'] = 'rlines'
                    if g['didasonly']:
                        g['stop'] = True
                        return
            break
        elif g['lines'][g['i'][0]][g['i'][1]] == 'l':
            g['mode'] = 'l'
            g['i'][1] += 1
        elif g['lines'][g['i'][0]][g['i'][1]] == 'c':
            g['mode'] = 'c'
            g['i'][1] += 1
        elif g['lines'][g['i'][0]][g['i'][1]] == 'r':
            g['mode'] = 'r'
            g['i'][1] += 1
        elif g['lines'][g['i'][0]][g['i'][1]] == ':':
            g['gmode'] = g['mode']
            g['shift'].insert(0, '')
            g['last_a'].insert(0, chr(ord('a')-1))
            g['i'][1] += 1
            if g['didasmode']:
                g['didasindent'] += 1

        elif g['lines'][g['i'][0]][g['i'][1]] == 'e':
            g['gmode'] = ''
            g['last_a'].pop(0)
            g['shift'].pop(0)
            g['i'][1] += 1
            g['shift'][0] = ''
            if g['didasmode']:
                g['didasindent'] -= 1
                if g['didasindent'] == 0:
                    g['out'] = 'rlines'
                    if g['didasonly']:
                        g['stop'] = True
                        return
        elif g['lines'][g['i'][0]][g['i'][1]] == 'p':
            g['shift'][0] += '   '
            g['i'][1] += 1
        elif g['lines'][g['i'][0]][g['i'][1]] == 'n':
            g['split'] = True
            g['i'][1] += 1
        elif g['lines'][g['i'][0]][g['i'][1]] == 'o':
            if g['sectionreg'] == 1:
                for e in g['sections']:
                    g[g['out']] += [e[0] + '\n']
            if g['sectionreg'] == 0:
                s = ''
                for e in g['shift']:
                    s += e
                s += '   '
                for e in g['sections']:
                    builder = s[:]
                    if e[0].find('.') == -1:
                        builder += e[0] + '.  '
                    else:
                        builder += ' '*(e[0].find('.')+1) + e[0][e[0].find('.')+1:] + '   '
                    if len(e[1]) < g['width']-len(builder)-len(e[2])-3:
                        builder += e[1] + ' ' + '.'*(g['width']-len(builder)-1-len(e[1])-len(e[2])) + e[2]+'\n'
                    else:
                        c = e[1].rfind(' ', 0, g['width']-len(builder)-len(e[2])-3)
                        builder += e[1][:c] + ' ' + '.'*(g['width']-len(builder)-c-1-len(e[2])) + e[2] + '\n'
                    g[g['out']] += [builder]
            g['i'][1] += 1
        elif g['lines'][g['i'][0]][g['i'][1]] == 's':
            g['last_a'] = [chr(ord('a')-1)]
            g['i'][1] += 1
            g['roz'] += 1
            g['pod'] = 0
            g['shift'][0] += str(g['roz']) + ' '
            if g['sectionreg'] == 2:
                g['sections'] += [[str(g['roz'])]]
                g['sectiontitle'] = True
            elif g['sectionreg'] == 1:
                for iterator in range(len(g['sections'])):
                    if len(g['sections'][iterator]) < 3:
                        g['sections'][iterator] += [str(int(g['v']['p'])+1)]
                        break
        elif g['lines'][g['i'][0]][g['i'][1]] == 'u':
            g['last_a'] = [chr(ord('a')-1)]
            g['i'][1] += 1
            g['pod'] += 1
            g['shift'][0] += str(g['roz']) + '.' + str(g['pod']) + ' '
            if g['sectionreg'] == 2:
                g['sections'] += [[str(g['roz']) + '.' + str(g['pod'])]]
                g['sectiontitle'] = True
            elif g['sectionreg'] == 1:
                for iterator in range(len(g['sections'])):
                    if len(g['sections'][iterator]) < 3:
                        g['sections'][iterator] += [str(int(g['v']['p'])+1)]
                        break
        elif g['lines'][g['i'][0]][g['i'][1]] == 'a':
            g['last_a'][0] = chr(ord(g['last_a'][0])+1)
            g['shift'][0] += g['last_a'][0]+') '
            g['i'][1] += 1
        elif g['lines'][g['i'][0]][g['i'][1]] == '-':
            g['shift'][0] += ' - '
            g['i'][1] += 1
        elif g['lines'][g['i'][0]][g['i'][1]] == '/':
            g['indented'] = True
            g['i'][1] += 1
        elif g['lines'][g['i'][0]][g['i'][1]] == 'h':
            g['iheader'] = g['i'].copy()
            g['didasmode'] = True
            g['didasindent'] = 0
            g['header'] = []
            g['out'] = 'header'
            g['i'][1] += 1
            g['shift'] = ['']
        elif g['lines'][g['i'][0]][g['i'][1]] == 'f':
            g['ifooter'] = g['i'].copy()
            g['didasmode'] = True
            g['didasindent'] = 0
            g['footer'] = []
            g['out'] = 'footer'
            g['i'][1] += 1
            g['shift'] = ['']
        elif g['lines'][g['i'][0]][g['i'][1]] == '\\':
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
        elif g['lines'][g['i'][0]][g['i'][1]] == '.':
            g[g['out']] += [g['fline']+'\n']
            g['fline'] = ''
            g['i'][1] += 1
        elif g['lines'][g['i'][0]][g['i'][1]] == '%':
            e = g['lines'][g['i'][0]][g['i'][1]+1:]
            if e.find('\"') == -1:
                g['i'][1] += 3
                g['v'][e[0]] = e[1]
            else:
                g['i'][1] += 1+len(e)
                g['v'][e[:e.find('\"')]] = e[e.find('\"')+1:]
        elif g['lines'][g['i'][0]][g['i'][1]] == '"':
            m = g['gmode']
            if g['mode'] != '':
                m = g['mode']
            s = ''
            for j in g['shift']:
                s = j + s
            w = g['width'] - len(s)
            e = g['lines'][g['i'][0]][g['i'][1]+1:]
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
                    g[g['out']] += [e[:c]+'\n']
                    f = find(g[g['out']][-1], '|')
                    g[g['out']][-1] = g[g['out']][-1].replace('||', '|')
                    if f != -1:
                        g['indent'] = ' '*f
                        g[g['out']][-1] = g[g['out']][-1][:f] + g[g['out']][-1][f+1:]
                        g['indented'] = True
                    for k in range(len(g['shift'])):
                        g['shift'][k] = len(g['shift'][k])*' '
                    s = ''
                    for j in g['shift']:
                        s = j + s
                    e = e[c+1:]
                    if g['sectiontitle']:
                        g['sections'][-1] += [g[g['out']][-1][len(s):-1]]
                        g['sectiontitle'] = False
                    inteligent = find(g[g['out']][-1], '\\')
                    if inteligent != -1:
                        if g['intsec']:
                            # ----------
                            ee = g[g['out']][-1][:inteligent]+(g['intmax']-len(g[g['out']][-1][:inteligent]))*' '+g[g['out']][-1][inteligent+1:]
                            ee = ee.replace('\n', '')
                            del g[g['out']][-1]
                            while True:
                                if len(ee) > g['width']:
                                    c = ee.rfind(' ', 0, 80)
                                else:
                                    c = len(ee)
                                g[g['out']] += [ee[:c] + '\n']
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
            g['i'][1] = len(g['lines'][g['i'][0]])
            g['shift'][0] = ''
            g['mode'] = ''
        else:
            print('WARN(', g['i'], '): don\'t know command ', g['lines'][g['i'][0]][g['i'][1]], ', skipping', sep='')
            g['i'][1] += 1


def interpreter(ai=False):
    global g
    t = True
    while (ai or t) and g['i'][0] < len(g['lines']):
        if g['i'][0] > 162:
            print(end='')
        if len(g['lines'][g['i'][0]]) == 0:
            g['rlines'] += ['\n']
            g['i'][0] += 1
        elif g['lines'][g['i'][0]][0] == '#':
            g['i'][0] += 1
        elif g['lines'][g['i'][0]][0] == '/':
            g['i'][1] = 1
            cmd()
            if g['stop']:
                g['stop'] = False
                return
        else:
            g['rlines'] += [g['lines'][g['i'][0]]+'\n']
            g['i'][0] += 1
        t = False
    return g['rlines']


def pagebuilder():
    global g
    g['page'] = ''
    while g['i'][0] < len(g['lines']):
        gbp = copy.deepcopy(g)
        # g BackuP
        interpreter()
        pagebp = g['page'][:]
        g['page'] += ''.join(g['rlines'])
        pagel = g['page'].splitlines(True)
        m = 110 - len(g['header']) - len(g['footer'])
        if g['v']['p'] == '0':
            m += len(g['header'])
        if len(pagel) > m or not g['i'][0] < len(g['lines']) or g['split']:
            if g['i'][0] < len(g['lines']) and not g['split']:
                g = gbp
            else:
                pagebp = g['page']
            g['split'] = False
            g['v']['p'] = str(int(g['v']['p'])+1)
            # header/footer update ------------
            gbp = copy.deepcopy(g)
            g['didasonly'] = True
            g['i'] = g['iheader']
            interpreter(True)
            g['didasonly'] = True
            g['i'] = g['ifooter']
            interpreter(True)
            header = g['header']
            footer = g['footer']
            g = gbp
            g['header'] = header
            g['footer'] = footer
            # ---------------------------------
            if g['v']['p'] != '1':
                g['pages'] += [g['header'] + pagebp.splitlines(True)]
            else:
                g['pages'] += [pagebp.splitlines(True)]
            g['pages'][-1] += ['\n'] * (110 - len(g['pages'][-1]) - len(g['footer'])) + g['footer']
            g['page'] = ''
        g['rlines'] = []
    out = []
    for e in g['pages']:
        out += e
    return out




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
        lines = fi.read().splitlines()
        greset()
        g['lines'] = lines[:]
        pagebuilder()
        sections = g['sections']
        greset()
        g['lines'] = lines[:]
        g['sectionreg'] = 1
        g['sections'] = sections
        pagebuilder()
        sections = g['sections']
        greset()
        g['lines'] = lines[:]
        g['sectionreg'] = 0
        g['sections'] = sections
        fo.writelines(pagebuilder())
    except FileNotFoundError:
        print('This file cannot be found...', file=sys.stderr)
        if len(sys.argv) > 1:
            print('Usage: ', sys.argv[0], ' [INPUT FILE] [OUTPUT FILE]', file=sys.stderr)
    finally:
        if 'fi' in locals():
            fi.close()
        if 'fo' in locals():
            fo.close()
