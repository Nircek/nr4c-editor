import sys
if __name__ == '__main__':
    try:
        if len(sys.argv) > 1:
            fi = open(sys.argv[1], 'r')
        else:
            fi = open(input('INPUT FILE: '), 'r')
        if len(sys.argv) > 2:
            fo = open(sys.argv[2], 'w')
        else:
            fo = open(input('OUTPUT FILE:'), 'w')
    except FileNotFoundError:
        print('This file cannot be found...', file=sys.stderr)
        if len(sys.argv) > 1:
            print('Usage: ', sys.argv[0], ' [INPUT FILE] [OUTPUT FILE]', file=sys.stderr)

        if 'fi' in locals():
            fi.close()
        if 'fo' in locals():
            fo.close()
