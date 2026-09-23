    def __init__(self, frame, buf=None, columns=None, col_space=None,
                 header=True, index=True, na_rep='NaN', formatters=None,
                 justify=None, float_format=None, sparsify=None,
                 index_names=True, line_width=None, max_rows=None,
                 max_cols=None, show_dimensions=False, **kwds):
        self.frame = frame
        self.buf = buf if buf is not None else StringIO()
        self.show_index_names = index_names

        if sparsify is None:
            sparsify = get_option("display.multi_sparse")

        self.sparsify = sparsify

        self.float_format = float_format
        self.formatters = formatters if formatters is not None else {}
        self.na_rep = na_rep
        self.col_space = col_space
        self.header = header
        self.index = index
        self.line_width = line_width
        self.max_rows = max_rows
        self.max_cols = max_cols
        self.max_rows_displayed = min(max_rows or len(self.frame),
                                      len(self.frame))
        self.show_dimensions = show_dimensions

        if justify is None:
            self.justify = get_option("display.colheader_justify")
        else:
            self.justify = justify

        self.kwds = kwds

        if columns is not None:
            self.columns = _ensure_index(columns)
            self.frame = self.frame[self.columns]
        else:
            self.columns = frame.columns
