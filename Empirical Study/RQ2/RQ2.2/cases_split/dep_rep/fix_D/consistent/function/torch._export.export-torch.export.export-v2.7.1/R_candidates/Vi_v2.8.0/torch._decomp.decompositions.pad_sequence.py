@register_decomposition(aten.pad_sequence.default)
@aten.pad_sequence.default.py_impl(DispatchKey.CompositeImplicitAutograd)
def pad_sequence(sequences, batch_first=False, padding_value=0.0):
    torch._check(len(sequences) > 0, lambda: "received an empty list of sequences")
    sequences_size = len(sequences)
    max_size = sequences[0].size()
    trailing_dims = max_size[1:]
    max_len = max(x.size(0) for x in sequences)
    if batch_first:
        out_dims = (sequences_size, max_len)
    else:
        out_dims = (max_len, sequences_size)
    out_dims = out_dims + trailing_dims
    out = sequences[0].new_full(out_dims, padding_value)
    dim_paddings = (0, 0) * len(trailing_dims)
    for i in range(sequences_size):
        currseq = sequences[i]
        row = aten.constant_pad_nd(
            currseq, dim_paddings + (0, max_len - currseq.size(0)), padding_value
        )
        if batch_first:
            out = aten.select_scatter(out, row, dim=0, index=i)
        else:
            out = aten.select_scatter(out, row, dim=1, index=i)
    return out
