def _gather_padding_ref(start_pad_width, end_pad_width, data, lengths):
    start_padding = np.zeros(data.shape[1:], dtype=data.dtype)
    end_padding = np.zeros(data.shape[1:], dtype=data.dtype)
    pad_width = start_pad_width + end_pad_width
    ptr = 0
    for length in lengths:
        for _ in range(start_pad_width):
            start_padding += data[ptr]
            ptr += 1
        ptr += length - pad_width
        for _ in range(end_pad_width):
            end_padding += data[ptr]
            ptr += 1
    return (start_padding, end_padding)
