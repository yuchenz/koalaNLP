import codecs
import sys

def trim(lines, long_th, short_th):
    """ Remove all sentences in lines that are longer than long_th,
    or shorter than short_th.
    """
    return [
        line for line in lines 
        if len(line.split()) >= short_th 
        and len(line.split()) <= long_th]

if __name__ == '__main__':
    short_threshold = sys.argv[1]
    long_threshold = sys.argv[2]
    filename = sys.argv[3]

    lines = codecs.open(filename, 'r', 'utf-8')

    print('longest sent: {}'.format(
        max([len(line.split()) for line in lines])))
    print('shortest sent: {}'.format(
        min([len(line.split()) for line in lines])))

    lines = trim(lines, long_threshold, short_threshold)

    with codecs.open(
        filename + '.trim[' + str(short_threshold) + '-' 
        + str(long_threshold) + ']', 'w', 'utf-8'
    ) as f:
        for line in lines:
            f.write(line)
