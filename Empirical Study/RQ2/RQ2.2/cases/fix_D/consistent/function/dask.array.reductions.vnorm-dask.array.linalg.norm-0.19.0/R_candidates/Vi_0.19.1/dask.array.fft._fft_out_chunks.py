def _fft_out_chunks(a, s, axes):
    """ For computing the output chunks of [i]fft*"""
    if s is None:
        return a.chunks
    chunks = list(a.chunks)
    for i, axis in enumerate(axes):
        chunks[axis] = (s[i],)
    return chunks
