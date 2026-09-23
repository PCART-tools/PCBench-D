    def __init__(self, *dtypes):
        super(disallow, self).__init__()
        self.dtypes = tuple(np.dtype(dtype).type for dtype in dtypes)
