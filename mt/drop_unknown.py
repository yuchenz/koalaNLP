import codecs
import sys


def drop_unknown(filename):
    lines = codecs.open(filename, 'r', 'utf-8').readlines()
    for line in lines:
        tmp = ''
        for char in line:
            if char <= '~': 
                tmp += char
        print(tmp, end='')


if __name__ == '__main__':
    filename = sys.argv[1]

    drop_unknown(filename)
