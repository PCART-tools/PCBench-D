    def _format_regular_rows(self) -> Iterable[ExcelCell]:
        if self._has_aliases or self.header:
            self.rowcounter += 1

        # output index and index_label?
        if self.index:
            # check aliases
            # if list only take first as this is not a MultiIndex
            if self.index_label and isinstance(
                self.index_label, (list, tuple, np.ndarray, Index)
            ):
                index_label = self.index_label[0]
            # if string good to go
            elif self.index_label and isinstance(self.index_label, str):
                index_label = self.index_label
            else:
                index_label = self.df.index.names[0]

            if isinstance(self.columns, MultiIndex):
                self.rowcounter += 1

            if index_label and self.header is not False:
                yield ExcelCell(self.rowcounter - 1, 0, index_label, self.header_style)

            # write index_values
            index_values = self.df.index
            if isinstance(self.df.index, PeriodIndex):
                index_values = self.df.index.to_timestamp()

            for idx, idxval in enumerate(index_values):
                yield ExcelCell(self.rowcounter + idx, 0, idxval, self.header_style)

            coloffset = 1
        else:
            coloffset = 0

        yield from self._generate_body(coloffset)
