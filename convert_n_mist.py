import numpy as np
import os
import concurrent.futures
import environment

np.set_printoptions(suppress=True)


def generate_2d_spikes(filename):
    '''
    Reads two dimensional binary spike file and returns a TD event.
    It is the same format used in neuromorphic datasets NMNIST & NCALTECH101.

    The binary file is encoded as follows:
        * Each spike event is represented by a 40 bit number.
        * First 8 bits (bits 39-32) represent the xID of the neuron.
        * Next 8 bits (bits 31-24) represent the yID of the neuron.
        * Bit 23 represents the sign of spike event: 0=>OFF event, 1=>ON event.
        * The last 23 bits (bits 22-0) represent the spike event timestamp in microseconds.

    Arguments:
        * ``filename`` (``string``): path to the binary file.

    Usage:

    '''
    with open(filename, 'rb') as inputFile:
        inputByteArray = inputFile.read()
    inputAsInt = np.asarray([x for x in inputByteArray])
    xEvent = inputAsInt[0::5].reshape(-1,1)
    yEvent = inputAsInt[1::5].reshape(-1,1)
    pEvent = inputAsInt[2::5] >> 7
    pEvent = pEvent.reshape(-1,1)
    tEvent = ((inputAsInt[2::5] << 16) | (inputAsInt[3::5] << 8) | (inputAsInt[4::5])) & 0x7FFFFF
    tEvent = tEvent.reshape(-1, 1)

    # return np.hstack((xEvent, yEvent, pEvent, tEvent / 1000)) # convert spike times to ms
    data = np.hstack((tEvent, xEvent, yEvent, pEvent))
    return data

def convert_bin_2_txt(source_path, target_path):
    data = generate_2d_spikes(source_path)
    np.savetxt(target_path, data, header='28 28', comments='', fmt='%d')


if __name__ == '__main__':
    for digit in os.listdir(environment.source_n_mnist_dir):
        if not os.path.exists(os.path.join(environment.target_n_mnist_dir, digit)):
            os.makedirs(os.path.join(environment.target_n_mnist_dir, digit))

    source_paths = []
    target_paths = []

    for digit in os.listdir(environment.source_n_mnist_dir):
        for file_name in os.listdir(os.path.join(environment.source_n_mnist_dir, digit)):
            file_path = os.path.join(environment.source_n_mnist_dir, digit, file_name)

            source_paths.append(file_path)
            target_paths.append(os.path.join(environment.target_n_mnist_dir, digit, file_name.split('.')[0]+'.txt'))
            # data = generate_2d_spikes(file_path)
            # np.savetxt(os.path.join(target_n_mnist_dir, digit, file_name.split('.')[0]+'.txt'), data, header='28 28', comments='', fmt='%d')


    with concurrent.futures.ProcessPoolExecutor() as executor:
        for result in executor.map(convert_bin_2_txt, source_paths, target_paths):
            #print(result)
            pass