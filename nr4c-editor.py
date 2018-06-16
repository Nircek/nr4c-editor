import sys


def cmd(lines, i, shift='', end='\n'):
    rlines = []
    f = False
    while not f:
        if not i[1] < len(lines[i[0]]):
            i[0] += 1
            i[1] = 0
            break
        if lines[i[0]][i[1]] == '"':
            rlines += [ str(shift + lines[i[0]][i[1]+1:] + end) ]
            i[1] = len(lines[i[0]])
        else:
            print('WARN: don\'t know command ', lines[i[0]][i[1]], ', skipping', sep='')
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
