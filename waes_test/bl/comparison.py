from data.data_layer import DataLayer
from logging import getLogger

logger = getLogger('waes')


def compare_files(id, data_layer=''):
    side = 'left'
    dl = data_layer if data_layer else DataLayer()
    try:
        left = dl.get(id, side)
        side = 'right'
        right = dl.get(id, side)
    except IOError:
        msg = 'File with id = %s and side = %s is not provided' % (id, side)
        raise IOError(msg)
    return compare(left, right)


def compare(left, right):
    # left length != right length
    if len(left) != len(right):
        return {'payload': 'Different length'}
    # left == right
    if left == right:
        return {'payload': 'Equal'}
    # left and right are diffrent
    out_data = []
    diff_counter = 0
    offset = -1
    for i in xrange(len(left)):

        if left[i] == right[i]:
            if diff_counter != 0:
                # if found equal symbols reset 
                # diff_counter and offset, save data
                out_data.append({'offset': offset, 'length': diff_counter})
                diff_counter = 0
                offset = -1
        else:
            if offset < 0:
                # if the first differnt synmbols save to offset the beginng
                offset = i
            diff_counter += 1

    if diff_counter > 0:
        out_data.append({'offset': offset, 'length': diff_counter})
    return {'payload': out_data}
