def _fft_wrap(fft_func, dtype, out_chunk_fn):
    def func(a, n=None, axis=-1):
        if len(a.chunks[axis]) != 1:
            raise ValueError(chunk_error % (axis, a.chunks[axis]))

        chunks = out_chunk_fn(a, n, axis)

        return map_blocks(partial(fft_func, n=n, axis=axis), a, dtype=dtype,
                          chunks=chunks)

    np_name = fft_func.__name__
    if fft_func.__doc__ is not None:
        func.__doc__ = (fft_preamble % (np_name, np_name)) + fft_func.__doc__
    func.__name__ = np_name
    return func
