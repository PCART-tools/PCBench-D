    @partial(normalize_token.register, np.ndarray)
    def normalize_array(x):
        if not x.shape:
            return (str(x), x.dtype)
        if hasattr(x, 'mode') and getattr(x, 'filename', None):
            return x.filename, os.path.getmtime(x.filename), x.dtype, x.shape
        if x.dtype.hasobject:
            try:
                data = md5('-'.join(x.flat).encode('utf-8')).hexdigest()
            except TypeError:
                data = md5(b'-'.join([str(item).encode() for item in x.flat])).hexdigest()
        else:
            try:
                data = md5(x.ravel().view('i1').data).hexdigest()
            except (BufferError, AttributeError, ValueError):
                data = md5(x.copy().ravel().view('i1').data).hexdigest()
        return (data, x.dtype, x.shape, x.strides)
