@normalize_token.register_lazy("numpy")
def register_numpy():
    import numpy as np

    @normalize_token.register(np.ndarray)
    def normalize_array(x):
        if not x.shape:
            return (str(x), x.dtype)
        if hasattr(x, 'mode') and getattr(x, 'filename', None):
            if hasattr(x.base, 'ctypes'):
                offset = (x.ctypes.get_as_parameter().value -
                          x.base.ctypes.get_as_parameter().value)
            else:
                offset = 0  # root memmap's have mmap object as base
            return (x.filename, os.path.getmtime(x.filename), x.dtype,
                    x.shape, x.strides, offset)
        if x.dtype.hasobject:
            try:
                data = md5('-'.join(x.flat).encode('utf-8')).hexdigest()
            except TypeError:
                data = md5(b'-'.join([unicode(item).encode('utf-8') for item in
                                      x.flat])).hexdigest()
        else:
            try:
                data = md5(x.ravel().view('i1').data).hexdigest()
            except (BufferError, AttributeError, ValueError):
                data = md5(x.copy().ravel().view('i1').data).hexdigest()
        return (data, x.dtype, x.shape, x.strides)

    normalize_token.register(np.dtype, repr)
    normalize_token.register(np.generic, repr)
