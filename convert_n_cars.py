import numpy as np
import os
import concurrent.futures
import environment
import sys

np.set_printoptions(suppress=True)

EV_TYPE = [('t', 'u4'), ('_', 'i4')]  # Event2D
def parse_header(f):
    """
    Parses the header of a dat file
    Args:
        - f file handle to a dat file
    return :
        - int position of the file cursor after the header
        - int type of event
        - int size of event in bytes
        - size (height, width) tuple of int or None
    """
    f.seek(0, os.SEEK_SET)
    bod = None
    end_of_header = False
    header = []
    num_comment_line = 0
    size = [None, None]
    # parse header
    while not end_of_header:
        bod = f.tell()
        line = f.readline()
        if sys.version_info > (3, 0):
            first_item = line.decode("latin-1")[:2]
        else:
            first_item = line[:2]

        if first_item != '% ':
            end_of_header = True
        else:
            words = line.split()
            if len(words) > 1:
                if words[1] == 'Date':
                    header += ['Date', words[2] + ' ' + words[3]]
                if words[1] == 'Height' or words[1] == b'Height':  # compliant with python 3 (and python2)
                    size[0] = int(words[2])
                    header += ['Height', words[2]]
                if words[1] == 'Width' or words[1] == b'Width':  # compliant with python 3 (and python2)
                    size[1] = int(words[2])
                    header += ['Width', words[2]]
            else:
                header += words[1:3]
            num_comment_line += 1
    # parse data
    f.seek(bod, os.SEEK_SET)

    if num_comment_line > 0:  # Ensure compatibility with previous files.
        # Read event type
        ev_type = np.frombuffer(f.read(1), dtype=np.uint8)[0]
        # Read event size
        ev_size = np.frombuffer(f.read(1), dtype=np.uint8)[0]
    else:
        ev_type = 0
        ev_size = sum([int(n[-1]) for _, n in EV_TYPE])

    bod = f.tell()
    return bod, ev_type, ev_size, size

def generate_2d_spikes(filename):
    _file = open(filename, "rb")

    _start, ev_type, _ev_size, _size = parse_header(_file)

    _file.seek(0, os.SEEK_END)
    _end = _file.tell()
    _ev_count = (_end - _start) // _ev_size
    _file.seek(_start)

    _decode_dtype = []
    for dtype in EV_TYPE:
        if dtype[0] == '_':
            _decode_dtype += [('x', 'u2'), ('y', 'u2'), ('p', 'u1')]
        else:
            _decode_dtype.append(dtype)

    dat = np.fromfile(_file, dtype=EV_TYPE, count=_ev_count)

    t = dat['t'][:, np.newaxis]
    x = np.bitwise_and(dat["_"], 16383)[:, np.newaxis]
    y = np.right_shift(np.bitwise_and(dat["_"], 268419072), 14)[:, np.newaxis]
    p = np.right_shift(np.bitwise_and(dat["_"], 268435456), 28)[:, np.newaxis]

    events = np.hstack((t, x, y, p))
    _file.close()
    return events

def convert_dat_2_txt(source_path, target_path):
    data = generate_2d_spikes(source_path)
    # todo 分辨率待定
    np.savetxt(target_path, data, header='180 180', comments='', fmt='%d')


if __name__ == '__main__':
    for train_test in environment.n_cars_train_test:
        for class_type in os.listdir(os.path.join(environment.source_n_cars_dir, train_test)):

            if not os.path.exists(os.path.join(environment.target_n_cars_dir, train_test, class_type)):
                os.makedirs(os.path.join(environment.target_n_cars_dir, train_test, class_type))

    source_paths = []
    target_paths = []

    for train_test in environment.n_cars_train_test:
        for class_type in os.listdir(os.path.join(environment.source_n_cars_dir, train_test)):
            index = 0
            for file_name in os.listdir(os.path.join(environment.source_n_cars_dir, train_test, class_type)):
                file_path = os.path.join(environment.source_n_cars_dir, train_test, class_type, file_name)
                index = index + 1
                # 每一类只保存 10 个
                if index == 10:
                    break
                source_paths.append(file_path)
                # print(os.path.join(environment.target_n_cars_dir, train_test, class_type, file_name.split('.')[0]+'.txt'))
                target_paths.append(os.path.join(environment.target_n_cars_dir, train_test, class_type, file_name.split('.')[0]+'.txt'))
            # data = generate_2d_spikes(file_path)
            # np.savetxt(os.path.join(target_n_mnist_dir, digit, file_name.split('.')[0]+'.txt'), data, header='28 28', comments='', fmt='%d')


    with concurrent.futures.ProcessPoolExecutor() as executor:
        for result in executor.map(convert_dat_2_txt, source_paths, target_paths):
            #print(result)
            pass