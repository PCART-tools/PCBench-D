    def _format_regular_rows(self):
        has_aliases = isinstance(self.header, (tuple, list, np.ndarray, Index))
        if has_aliases or self.header:
            self.rowcounter += 1

        coloffset = 0
        # output index and index_label?
        if self.index:
            # chek aliases
            # if list only take first as this is not a MultiIndex
            if self.index_label and isinstance(self.index_label,
                                               (list, tuple, np.ndarray, Index)):
                index_label = self.index_label[0]
            # if string good to go
            elif self.index_label and isinstance(self.index_label, str):
                index_label = self.index_label
            else:
                index_label = self.df.index.names[0]

            if index_label and self.header is not False:
                if self.merge_cells:
                    yield ExcelCell(self.rowcounter,
                                    0,
                                    index_label,
                                    header_style)
                    self.rowcounter += 1
                else:
                    yield ExcelCell(self.rowcounter - 1,
                                    0,
                                    index_label,
                                    header_style)

            # write index_values
            index_values = self.df.index
            if isinstance(self.df.index, PeriodIndex):
                index_values = self.df.index.to_timestamp()

            coloffset = 1
            for idx, idxval in enumerate(index_values):
                yield ExcelCell(self.rowcounter + idx, 0, idxval, header_style)

        # Get a frame that will account for any duplicates in the column names.
        col_mapped_frame = self.df.loc[:, self.columns]

        # Write the body of the frame data series by series.
        for colidx in range(len(self.columns)):
            series = col_mapped_frame.iloc[:, colidx]
            for i, val in enumerate(series):
                yield ExcelCell(self.rowcounter + i, colidx + coloffset, val)
