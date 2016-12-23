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
    raw_data_wo_space = ''.join(raw_data.strip().split())
    processed_data = read_data_from_dir(processed_dir)
    processed_data_wo_space = ''.join(processed_data.strip().split())

    return (len(processed_data), len(raw_data), 
        len(raw_data_wo_space), len(processed_data_wo_space))


if __name__ == '__main__':
    raw_dir = sys.argv[1]
    processed_dir = sys.argv[2]

    process_count1, raw_count1, raw_count2, process_count2 = char_loss_rate(
        raw_dir, processed_dir)

    print("raw characters: {}, without spaces: {}".format(
        raw_count1, raw_count2))
    print("processed characters: {}, without spaces: {}".format(
        process_count1, process_count2))
    print("loss rate: {:.2%}, without spaces: {:.2%}".format(
        (raw_count1 - process_count1) / raw_count1,
        (raw_count2 - process_count2) / raw_count2))
