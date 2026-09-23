    def __init__(self, series, buf=None, length=True, header=True,
                 na_rep='NaN', name=False, float_format=None, dtype=True,
                 max_rows=None):
        self.series = series
        self.buf = buf if buf is not None else StringIO()
        self.name = name
        self.na_rep = na_rep
        self.header = header
        self.length = length
        self.max_rows = max_rows

        if float_format is None:
            float_format = get_option("display.float_format")
        self.float_format = float_format
        self.dtype = dtype

        self._chk_truncate()
