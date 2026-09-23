@wraps(np.reshape)
def reshape(array, shape):
    from .slicing import sanitize_index

    shape = tuple(map(sanitize_index, shape))
    known_sizes = [s for s in shape if s != -1]
    if len(known_sizes) < len(shape):
        if len(known_sizes) - len(shape) > 1:
            raise ValueError('can only specify one unknown dimension')
        missing_size = sanitize_index(array.size / reduce(mul, known_sizes, 1))
        shape = tuple(missing_size if s == -1 else s for s in shape)

    if reduce(mul, shape, 1) != array.size:
        raise ValueError('total size of new array must be unchanged')

    # ensure the same number of leading dimensions of size 1, to simply the
    # logic below
    leading_ones_diff = 0
    for size in array.shape:
        if size != 1:
            break
        leading_ones_diff += 1
    for size in shape:
        if size != 1:
            break
        leading_ones_diff -= 1

    if leading_ones_diff > 0:
        array = array[(0,) * leading_ones_diff]
    elif leading_ones_diff < 0:
        array = array[(np.newaxis,) * -leading_ones_diff]

    # leading dimensions with the same size can be ignored in the reshape
    ndim_same = 0
    for old_size, new_size in zip(array.shape, shape):
        if old_size != new_size:
            break
        ndim_same += 1

    if any(len(c) != 1 for c in array.chunks[ndim_same + 1:]):
        raise ValueError('dask.array.reshape requires that reshaped '
                         'dimensions after the first contain at most one chunk')

    if ndim_same == len(shape):
        chunks = array.chunks[:ndim_same]
    elif ndim_same == array.ndim:
        chunks = (array.chunks[:ndim_same] +
                  tuple((c,) for c in shape[ndim_same:]))
    else:
        trailing_size_before = reduce(mul, array.shape[ndim_same + 1:], 1)
        trailing_size_after = reduce(mul, shape[ndim_same + 1:], 1)

        ndim_same_chunks, remainders = zip(
            *(divmod(c * trailing_size_before, trailing_size_after)
              for c in array.chunks[ndim_same]))

        if any(remainder != 0 for remainder in remainders):
            raise ValueError('dask.array.reshape requires that the first '
                             'reshaped dimension can be evenly divided into '
                             'new chunks')

        chunks = (array.chunks[:ndim_same] + (ndim_same_chunks, )
                  + tuple((c, ) for c in shape[ndim_same + 1:]))

    name = 'reshape-' + tokenize(array, shape)

    dsk = {}
    prev_index_count = min(ndim_same + 1, array.ndim, len(shape))
    extra_zeros = len(shape) - prev_index_count
    for key in core.flatten(array._keys()):
        index = key[1:]
        valid_index = index[:prev_index_count]
        new_key = (name,) + valid_index + (0,) * extra_zeros
        new_shape = (tuple(chunk[i] for i, chunk in zip(valid_index, chunks))
                     + shape[prev_index_count:])
        dsk[new_key] = (np.reshape, key, new_shape)

    return Array(merge(dsk, array.dask), name, chunks, dtype=array.dtype)
