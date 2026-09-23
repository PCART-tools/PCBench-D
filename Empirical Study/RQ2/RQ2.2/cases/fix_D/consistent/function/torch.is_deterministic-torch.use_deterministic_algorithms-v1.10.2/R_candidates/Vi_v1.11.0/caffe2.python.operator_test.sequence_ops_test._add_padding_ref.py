def _add_padding_ref(
        start_pad_width, end_pad_width, ret_lengths,
        data, lengths, start_padding=None, end_padding=None):
    if start_padding is None:
        start_padding = np.zeros(data.shape[1:], dtype=data.dtype)
    end_padding = (
        end_padding if end_padding is not None else start_padding)
    out_size = data.shape[0] + (
        start_pad_width + end_pad_width) * len(lengths)
    out = np.ndarray((out_size,) + data.shape[1:])
    in_ptr = 0
    out_ptr = 0
    for length in lengths:
        out[out_ptr:(out_ptr + start_pad_width)] = start_padding
        out_ptr += start_pad_width
        out[out_ptr:(out_ptr + length)] = data[in_ptr:(in_ptr + length)]
        in_ptr += length
        out_ptr += length
        out[out_ptr:(out_ptr + end_pad_width)] = end_padding
        out_ptr += end_pad_width
    lengths_out = lengths + (start_pad_width + end_pad_width)
    if ret_lengths:
        return (out, lengths_out)
    else:
        return (out, )
