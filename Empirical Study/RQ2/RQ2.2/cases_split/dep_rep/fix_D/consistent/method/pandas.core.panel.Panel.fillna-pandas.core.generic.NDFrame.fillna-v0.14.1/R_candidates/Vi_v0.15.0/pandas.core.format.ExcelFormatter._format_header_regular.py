    def _format_header_regular(self):
        has_aliases = isinstance(self.header, (tuple, list, np.ndarray, Index))
        if has_aliases or self.header:
            coloffset = 0

            if self.index:
                coloffset = 1
                if isinstance(self.df.index, MultiIndex):
                    coloffset = len(self.df.index[0])

            colnames = self.columns
            if has_aliases:
                if len(self.header) != len(self.columns):
                    raise ValueError(('Writing %d cols but got %d aliases'
                                      % (len(self.columns), len(self.header))))
                else:
                    colnames = self.header

            for colindex, colname in enumerate(colnames):
                yield ExcelCell(self.rowcounter, colindex + coloffset, colname,
                                header_style)
