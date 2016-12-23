import codecs
import sys
import os


def read_data_from_dir(directory):
    data = ''
    for filename in os.listdir(directory):
        data += codecs.open(
            os.path.join(directory, filename), 'r', 'utf-8').read()
    return data


def char_loss_rate(raw_dir, processed_dir):
    ''' When pre-processing text data, we sometimes lose some data.
    This function computes the loss rate of characters, given the directory
    of the raw data before pre-processing, and the directory of the
    pre-processed data.
    '''
    raw_data = read_data_from_dir(raw_dir)
    processed_data = read_data_from_dir(processed_dir)

    return len(processed_data), len(raw_data)


if __name__ == '__main__':
    raw_dir = sys.argv[1]
    processed_dir = sys.argv[2]

    processed_char_count, raw_char_count = char_loss_rate(
        raw_dir, processed_dir)

    print("raw characters: {}".format(raw_char_count))
    print("processed characters: {}".format(processed_char_count))
    print("loss rate: {:.2%}".format(
        (raw_char_count - processed_char_count) / raw_char_count))
