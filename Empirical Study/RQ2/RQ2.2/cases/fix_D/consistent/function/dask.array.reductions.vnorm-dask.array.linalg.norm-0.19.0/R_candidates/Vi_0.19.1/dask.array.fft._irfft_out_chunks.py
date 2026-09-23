def _irfft_out_chunks(a, s, axes):
    """ For computing the output chunks of irfft*"""
    if s is None:
        s = [a.chunks[axis][0] for axis in axes]
        s[-1] = 2 * (s[-1] - 1)
    chunks = list(a.chunks)
    for i, axis in enumerate(axes):
        chunks[axis] = (s[i],)
    return chunks
