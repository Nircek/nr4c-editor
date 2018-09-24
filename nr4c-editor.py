#!/usr/bin/env python3
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
        'lines': [],            # var containing input
        'width': 80,            # max width of output line
        'rlines': [],           # var containing output lines
        'gmode': '',            # global mode (before indention)
        'mode': '',             # mode (left, right or center)
        'i': [0, 0],            # var containing file iter
        'shift': [''],          # array containing shifts (with indention)
        'last_a': [chr(ord('a')-1)],    # last a) bullet
        'fline': '',            # formatting line
        'roz': 0,               # section nr
        'pod': 0,               # subsection nr
        'v': {                  # variables
            'D': datetime.date.today().strftime('%#d %B %Y'), # full date
            'd': datetime.date.today().strftime('%Y-%m-%d'), # short date
            'p': '0',           # last page nr
            'l': '\n',          # new line
            'nl': '\r'          # no new line
        },
        'indent': '',           # forced indent
        'indented': False,      # use forced indent?
        'intfirst': (),         # info about first intelligent tab occurrence
        'intmax': 0,            # max caught intelligent indent
        'intsec': False,        # is it second circulation of intelligent tab
        'didasmode': False,
        'didasindent': 0,
        'didasonly': False,
        'stop': False,          # stops interpreting (useful to hf-only mode)
        'out': 'rlines',
        'iheader': None,        # iteration where last header was caught
        'header': [],           # last caught header
        'ifooter': None,        # iteration where last footer was caught
        'footer': [],           # last caught footer
        'split': False,         # splits page now
        'pages': [],
        'sections': [],         # list of caught sections
        'sectiontitle': False,  # instruction "catch section title" for ToC
        'sectionreg': 2,        # sections registering mode
        # 2 = collecting names
        # 1 = collecting pages
        # 0 = no collecting
        'title': [],            # caught title for next paragraph
        'titled': False         # instruction "catch title" for protection against page splitting separately with body
    }


def find(st, s):
    """
    A string find, that ignore results with double first character
    :param st: string, where we are looking for
    :param s: string, what we are looking for
    :return: indec, where s was found
    """
    i = 0
    if len(s) >= 2:
        if s[0] == s[1]:
            raise ValueError('this is not possible to find string with double first character')
            # because doubled first characters are ignored
    st = st.replace(s[0]*2, '')
    return st.find(s, i)


def cmd():
    global g
    while True:
        if not g['i'][1] < len(g['lines'][g['i'][0]]):  # if it's end of line
            g['i'][0] += 1                              # jump to next line
            g['i'][1] = 0
            g['indented'] = False
            if g['didasmode']:
                if g['didasindent'] == 0:               # if it's end of didas (only when we have one-line didas)
                    g['out'] = 'rlines'                 # start outputting to 'rlines'
                    if g['didasonly']:                  # if didasonly:
                        g['stop'] = True                # stop interpreting
                        return
            break
        elif g['lines'][g['i'][0]][g['i'][1]] == 'l':   # if command is l
            g['mode'] = 'l'                             # set mode to l
            g['i'][1] += 1  # jump to next character
        elif g['lines'][g['i'][0]][g['i'][1]] == 'c':   # if command is c
            g['mode'] = 'c'                             # set mode to c
            g['i'][1] += 1
        elif g['lines'][g['i'][0]][g['i'][1]] == 'r':
            g['mode'] = 'r'
            g['i'][1] += 1
        elif g['lines'][g['i'][0]][g['i'][1]] == ':':   # if cmd is :
            g['gmode'] = g['mode']
            g['shift'].insert(0, '')
            g['last_a'].insert(0, chr(ord('a')-1))
            g['i'][1] += 1
            if g['didasmode']:                          # if didasmode:
                g['didasindent'] += 1                   # increment indent counter

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
            g['shift'][0] += '   '                      # add indent
            g['i'][1] += 1
        elif g['lines'][g['i'][0]][g['i'][1]] == 'n':
            g['split'] = True
            g['i'][1] += 1
        elif g['lines'][g['i'][0]][g['i'][1]] == 'o':
            if g['titled'] and g['out'] == 'rlines':    # /* if ToC has title
                g['rlines'] += g['title']               # print it
                g['title'] = []
                g['titled'] = False                     # */
            if g['sectionreg'] == 1:                    # if we are collecting nr of pages
                for e in g['sections']:
                    g[g['out']] += [e[0] + '\n']        # print all names to shift rest and update page numbers
            if g['sectionreg'] == 0:                    # if we are printing final ToC
                s = ''
                for e in g['shift']:                    # calculate indent
                    s += e
                s += '   '                              # and add our indent
                for e in g['sections']:                 # for each element in ToC
                    builder = s[:]                      # print indent
                    e[1] = e[1].replace('\r', '')       # delete %nl
                    if e[0].find('.') != -1:            # if it's subsection
                        builder += ' '*(e[0].find('.')+1) + e[0][e[0].find('.')+1:]  # delete section nr, print sub nr
                        builder += (7+len(s)-len(builder))*' '  # and add 7 spaces padding
                    elif e[0] == '':                    # if it's title
                        builder += (5+len(s)-len(builder))*' '  # add 5 spaces padding
                    else:                               # if it's section
                        builder += e[0] + '.'           # print section nr with dot
                        builder += (5+len(s)-len(builder))*' '  # add 5 spaces padding
                    if len(e[1]) < g['width']-len(builder)-len(e[2])-3:  # if whole name fits
                        builder += e[1] + ' ' + '.'*(g['width']-len(builder)-1-len(e[1])-len(e[2])) + e[2]+'\n'
                        # print name with dot leader and page nr at end
                    else:                               # if not
                        c = e[1].rfind(' ', 0, g['width']-len(builder)-len(e[2])-3)  # cut the name
                        builder += e[1][:c] + ' ' + '.'*(g['width']-len(builder)-c-1-len(e[2])) + e[2] + '\n'
                        # print cut name with dot leader and page nr at end
                    g[g['out']] += [builder]
            g['i'][1] += 1
        elif g['lines'][g['i'][0]][g['i'][1]] == 's':
            g['last_a'] = [chr(ord('a')-1)]             # reset last_a
            g['i'][1] += 1
            g['roz'] += 1                               # increment section iter
            g['pod'] = 0                                # reset sub iter
            g['shift'][0] += str(g['roz']) + ' '        # add section padding
            g['out'] = 'title'                          # print name with text below it
            g['titled'] = True
            if g['sectionreg'] == 2:                    # if collecting names
                g['sections'] += [[str(g['roz'])]]      # collect them
                g['sectiontitle'] = True                # next text is title of section
            elif g['sectionreg'] == 1:                  # if collecting page nr
                for iterator in range(len(g['sections'])):  # search for section
                    if len(g['sections'][iterator]) < 3:  # which has no page nr
                        g['sections'][iterator] += [str(int(g['v']['p'])+1)]  # and add page nr
                        break
        elif g['lines'][g['i'][0]][g['i'][1]] == 't':
            # g['last_a'] = [chr(ord('a')-1)]
            g['i'][1] += 1
            # g['roz'] += 1
            # g['pod'] = 0
            # g['shift'][0] += str(g['roz']) + ' '
            if g['sectionreg'] == 2:
                g['sections'] += [['']]
                g['sectiontitle'] = True
            elif g['sectionreg'] == 1:
                for iterator in range(len(g['sections'])):
                    if len(g['sections'][iterator]) < 3:
                        g['sections'][iterator] += [str(int(g['v']['p'])+1)]
                        break
            g['out'] = 'title'
            g['titled'] = True
        elif g['lines'][g['i'][0]][g['i'][1]] == 'k':
            g['out'] = 'title'
            g['titled'] = True
            g['i'][1] += 1
        elif g['lines'][g['i'][0]][g['i'][1]] == 'u':
            g['last_a'] = [chr(ord('a')-1)]
            g['i'][1] += 1
            g['pod'] += 1
            g['out'] = 'title'
            g['titled'] = True
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
            g['last_a'][0] = chr(ord(g['last_a'][0])+1)     # increment bullet
            g['shift'][0] += g['last_a'][0]+') '            # add indent
            g['i'][1] += 1
        elif g['lines'][g['i'][0]][g['i'][1]] == '-':
            g['shift'][0] += ' - '                          # add indent
            g['i'][1] += 1
        elif g['lines'][g['i'][0]][g['i'][1]] == '/':
            g['indented'] = True                            # force collected indent
            g['i'][1] += 1
        elif g['lines'][g['i'][0]][g['i'][1]] == 'h':
            g['iheader'] = g['i'].copy()                    # remember place of header in input
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
            if g['intsec']:             # if after all
                g['intmax'] = 0         # reset
                g['intfirst'] = ()
                g['i'][1] += 1
            else:                       # if not
                intsec = g['intsec']
                intmax = g['intmax']
                g = g['intfirst']       # turn back time to first call
                # g['i'][1] = 1
                g['intsec'] = intsec
                g['intmax'] = intmax    # but remember indent
            g['intsec'] = not g['intsec']
        elif g['lines'][g['i'][0]][g['i'][1]] == '.':
            g[g['out']] += [g['fline']+'\n']  # print formatted line
            g['fline'] = ''                   # and reset it
            g['i'][1] += 1
        elif g['lines'][g['i'][0]][g['i'][1]] == '%':
            e = g['lines'][g['i'][0]][g['i'][1]+1:]  # collect following text
            if e.find('\"') == -1:  # if it has no text
                g['i'][1] += 3
                g['v'][e[0]] = e[1]  # collect next single characters (%%) as %=%
            else:
                g['i'][1] += 1+len(e)       # go to end of line
                g['v'][e[:e.find('\"')]] = e[e.find('\"')+1:]   # and collect all (%"%) as %=%
        elif g['lines'][g['i'][0]][g['i'][1]] == '"':
            if g['titled'] and g['out'] == 'rlines':    # if has title
                g['rlines'] += g['title']               # print it
                g['title'] = []
                g['titled'] = False
            m = g['gmode']

            if g['mode'] != '':
                m = g['mode']                           # calculate mode

            s = ''
            for j in g['shift']:
                s = j + s                               # calculate indent

            w = g['width'] - len(s)                     # calculate real space for alignment

            e = g['lines'][g['i'][0]][g['i'][1]+1:]     # get following text

            for elem in g['v'].items():                 # /* change variables to values
                while True:
                    f = find(e, '%'+elem[0])
                    if f == -1:
                        break
                    e = e[:f] + elem[1] + e[f+len(elem[0])+1:]
            e = e.replace('%%', '%')                    # and suppress escaped

            if m == '':                                 # if no alignment
                while e != '':                          # while there's text
                    if g['indented']:
                        s = g['indent']                 # force indent if so

                    e = s + e                           # add indent to text

                    if len(e) > g['width']:             # if text is too long for one line
                        c = e.rfind(' ', 0, 80)         # cut after last fitted space
                    else:
                        c = len(e)                      # get all text

                    inteligent = find(e, '\\')
                    if inteligent != -1 and g['intfirst'] == () and not g['intsec']:  # if first occurrence
                        g['intfirst'] = copy.deepcopy(g)  # save current state

                    g[g['out']] += [e[:c]+'\n']         # print to output
                    f = find(g[g['out']][-1], '|')      # find |
                    g[g['out']][-1] = g[g['out']][-1].replace('||', '|')  # and suppress escaped
                    if f != -1:                         # if | is found
                        g['indent'] = ' '*f             # set indent for wrapped lines
                        g[g['out']][-1] = g[g['out']][-1][:f] + g[g['out']][-1][f+1:]  # suppress |
                        g['indented'] = True            # set forced indent for wrapped lines

                    for k in range(len(g['shift'])):
                        g['shift'][k] = len(g['shift'][k])*' '  # replace indent with spaces (change "a) -" to "    ")

                    s = ''
                    for j in g['shift']:
                        s = j + s                       # calculate new indent

                    e = e[c+1:]                         # get remaining (wrapped) text

                    if g['sectiontitle']:               # if you're catching section tile
                        g['sections'][-1] += [g[g['out']][-1][len(s):-1]]  # catch
                        g['sectiontitle'] = False  # and stop catching

                    inteligent = find(g[g['out']][-1], '\\')
                    if inteligent != -1:                # if found calling intelligent tab
                        if g['intsec']:                 # if it's second circulation
                            ee = g[g['out']][-1][:inteligent] + (g['intmax']-len(g[g['out']][-1][:inteligent]))*' ' + \
                                 g[g['out']][-1][inteligent+1:]  # add intelligent tab
                            ee = ee.replace('\n', '')   # delete new line char
                            del g[g['out']][-1]         # delete original
                            while True:                 # /* wrap lines with intelligent indent
                                if len(ee) > g['width']:
                                    c = ee.rfind(' ', 0, 80)
                                else:
                                    c = len(ee)
                                g[g['out']] += [ee[:c] + '\n']
                                if e == '':
                                    break
                                ee = g['intmax']*' ' + ee  # */

                        else:

                            g['intmax'] = max(g['intmax'], inteligent)  # update max collected intelligent indent

                if g['out'] == 'title':  # if you were collecting title
                    if g['title'][-1][-2] == '\r':
                        g['title'][-1] = g['title'][-1][:-2] + '\n'
                    else:
                        g['title'] += ['\n']
                    g['out'] = 'rlines'
            else:                                               # if we must do alignment

                if g['fline'] == '':
                    g['fline'] = s + ' '*w
                    for k in range(len(g['shift'])):
                        g['shift'][k] = len(g['shift'][k])*' '  # initialize fline var

                # ml - length of inserting text
                # mf - first index for inserting text
                # me - last index for inserting text
                ml = len(e)                                     # /* calculations
                if m == 'l':
                    mf = len(s)
                    me = len(s) + ml
                elif m == 'r':
                    mf = g['width'] - ml
                    me = g['width']
                elif m == 'c':
                    mf = len(s) + (w-ml)//2
                    me = mf + ml                                # */

                if g['fline'][mf:me] != ml * ' ':               # covering warning
                    print('WARN(', g['i'], '): covering \'', g['fline'][mf:me], '\' by \'', e, '\'', sep='')

                g['fline'] = g['fline'][:mf] + e + g['fline'][me:]  # update fline var after calculations

            g['i'][1] = len(g['lines'][g['i'][0]])              # go to end of line
            g['shift'][0] = ''                                  # reset local indent
            g['mode'] = ''                                      # reset local mode

        else:                                                   # if we don't recognize this command
                                                                # print warning
            print('WARN(', g['i'], '): don\'t know command ', g['lines'][g['i'][0]][g['i'][1]], ', skipping', sep='')
            g['i'][1] += 1


def interpreter(ai=False):
    global g
    t = True                # is first circulation
    while (ai or t) and g['i'][0] < len(g['lines']):
        if g['i'][0] > 134:
            print(end='')  # to stop debugging here
        if len(g['lines'][g['i'][0]]) == 0:     # if it's raw newline
            g['rlines'] += ['\n']
            g['i'][0] += 1
        elif g['lines'][g['i'][0]][0] == '#':   # if it's comment
            g['i'][0] += 1
        elif g['lines'][g['i'][0]][0] == '/':   # if it's command
            g['i'][1] = 1
            cmd()                               # interpret this
            if g['stop']:
                g['stop'] = False               # stop recognizing
                return
        else:                                   # if it's raw
            g['rlines'] += [g['lines'][g['i'][0]]+'\n']
            g['i'][0] += 1
        t = False
    return g['rlines']


def pagebuilder():
    global g
    g['page'] = ''
    while g['i'][0] < len(g['lines']):                      # if it is not end of file
        gbp = copy.deepcopy(g)
        # g BackuP
        interpreter()
        pagebp = g['page'][:]
        g['page'] += ''.join(g['rlines'])
        pagel = g['page'].splitlines(True)
        m = 110 - len(g['header']) - len(g['footer'])
        if g['v']['p'] == '0':
            m += len(g['header'])
        if len(pagel) > m or not g['i'][0] < len(g['lines']) or g['split']:  # if it's over page limit
            if g['i'][0] < len(g['lines']) and not g['split']:
                g = gbp                                     # get last state
            else:
                pagebp = g['page']
            g['split'] = False
            g['v']['p'] = str(int(g['v']['p'])+1)           # update page nr

            gbp = copy.deepcopy(g)                          # /* header and footer update
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
            g['footer'] = footer                            # */

            if g['v']['p'] != '1':                          # if not first page
                g['pages'] += [g['header'] + pagebp.splitlines(True)]  # add header
            else:
                g['pages'] += [pagebp.splitlines(True)]
            # pad to page height and add footer
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
            fo = open(sys.argv[2], 'w', encoding='utf-8', newline='\r\n')
        else:
            fo = open(input('OUTPUT FILE: '), 'w', encoding='utf-8', newline='\r\n')
        lines = fi.read().splitlines()
        greset()
        g['lines'] = lines[:]
        pagebuilder()                       # collect names
        sections = g['sections']
        greset()
        g['lines'] = lines[:]
        g['sectionreg'] = 1
        g['sections'] = sections
        pagebuilder()                       # collect page numbers
        sections = g['sections']
        greset()
        g['lines'] = lines[:]
        g['sectionreg'] = 0
        g['sections'] = sections
        fo.writelines(pagebuilder())        # interpret
    except FileNotFoundError:
        print('This file cannot be found...', file=sys.stderr)
        if len(sys.argv) > 1:
            print('Usage: ', sys.argv[0], ' [INPUT FILE] [OUTPUT FILE]', file=sys.stderr)
    finally:
        if 'fi' in locals():
            fi.close()
        if 'fo' in locals():
            fo.close()
