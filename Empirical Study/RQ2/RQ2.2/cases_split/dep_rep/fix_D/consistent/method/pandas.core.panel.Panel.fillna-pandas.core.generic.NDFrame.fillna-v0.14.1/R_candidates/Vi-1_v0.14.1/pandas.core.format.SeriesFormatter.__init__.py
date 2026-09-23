    def __init__(self, series, buf=None, header=True, length=True,
                 na_rep='NaN', name=False, float_format=None, dtype=True):
        self.series = series
        self.buf = buf if buf is not None else StringIO()
        self.name = name
        self.na_rep = na_rep
        self.length = length
        self.header = header

        if float_format is None:
            float_format = get_option("display.float_format")
        self.float_format = float_format
        self.dtype = dtype
