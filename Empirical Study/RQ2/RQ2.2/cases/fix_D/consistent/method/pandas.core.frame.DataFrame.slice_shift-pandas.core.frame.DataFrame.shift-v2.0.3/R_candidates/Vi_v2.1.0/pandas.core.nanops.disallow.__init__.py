    def __init__(self, *dtypes: Dtype) -> None:
        super().__init__()
        self.dtypes = tuple(pandas_dtype(dtype).type for dtype in dtypes)
