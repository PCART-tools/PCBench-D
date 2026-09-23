def _remove_padding_ref(start_pad_width, end_pad_width, data, lengths):
    pad_width = start_pad_width + end_pad_width
    out_size = data.shape[0] - (
        start_pad_width + end_pad_width) * len(lengths)
    out = np.ndarray((out_size,) + data.shape[1:])
    in_ptr = 0
    out_ptr = 0
    for length in lengths:
        out_length = length - pad_width
        out[out_ptr:(out_ptr + out_length)] = data[
            (in_ptr + start_pad_width):(in_ptr + length - end_pad_width)]
        in_ptr += length
        out_ptr += out_length
    lengths_out = lengths - (start_pad_width + end_pad_width)
    return (out, lengths_out)
