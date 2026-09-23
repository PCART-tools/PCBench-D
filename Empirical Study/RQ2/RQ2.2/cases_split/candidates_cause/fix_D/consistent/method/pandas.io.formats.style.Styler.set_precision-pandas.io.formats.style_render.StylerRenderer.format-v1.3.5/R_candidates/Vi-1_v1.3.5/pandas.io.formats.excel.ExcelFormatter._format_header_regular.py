    def _format_header_regular(self) -> Iterable[ExcelCell]:
        if self._has_aliases or self.header:
            coloffset = 0

            if self.index:
                coloffset = 1
                if isinstance(self.df.index, MultiIndex):
                    coloffset = len(self.df.index[0])

            colnames = self.columns
            if self._has_aliases:
                self.header = cast(Sequence, self.header)
                if len(self.header) != len(self.columns):
                    raise ValueError(
                        f"Writing {len(self.columns)} cols "
                        f"but got {len(self.header)} aliases"
                    )
                else:
                    colnames = self.header

            for colindex, colname in enumerate(colnames):
                yield ExcelCell(
                    self.rowcounter, colindex + coloffset, colname, self.header_style
                )
