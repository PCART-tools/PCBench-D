def _hfft_out_chunks(a, s, axes):
    assert len(axes) == 1

    axis = axes[0]

    if s is None:
        s = [2 * (a.chunks[axis][0] - 1)]

    n = s[0]

    chunks = list(a.chunks)
    chunks[axis] = (n,)
    return chunks
