    def _format_hierarchical_rows(self):
        has_aliases = isinstance(self.header, (tuple, list, np.ndarray, Index))
        if has_aliases or self.header:
            self.rowcounter += 1

        gcolidx = 0

        if self.index:
            index_labels = self.df.index.names
            # check for aliases
            if self.index_label and isinstance(self.index_label,
                                               (list, tuple, np.ndarray, Index)):
                index_labels = self.index_label

            # if index labels are not empty go ahead and dump
            if (any(x is not None for x in index_labels)
                    and self.header is not False):

                if not self.merge_cells:
                    self.rowcounter -= 1

                for cidx, name in enumerate(index_labels):
                    yield ExcelCell(self.rowcounter,
                                    cidx,
                                    name,
                                    header_style)
                self.rowcounter += 1

            if self.merge_cells:
                # Format hierarchical rows as merged cells.
                level_strs = self.df.index.format(sparsify=True, adjoin=False,
                                                  names=False)
                level_lengths = _get_level_lengths(level_strs)

                for spans, levels, labels in zip(level_lengths,
                                                 self.df.index.levels,
                                                 self.df.index.labels):
                    values = levels.take(labels)
                    for i in spans:
                        if spans[i] > 1:
                            yield ExcelCell(self.rowcounter + i,
                                            gcolidx,
                                            values[i],
                                            header_style,
                                            self.rowcounter + i + spans[i] - 1,
                                            gcolidx)
                        else:
                            yield ExcelCell(self.rowcounter + i,
                                            gcolidx,
                                            values[i],
                                            header_style)
                    gcolidx += 1

            else:
                # Format hierarchical rows with non-merged values.
                for indexcolvals in zip(*self.df.index):
                    for idx, indexcolval in enumerate(indexcolvals):
                        yield ExcelCell(self.rowcounter + idx,
                                        gcolidx,
                                        indexcolval,
                                        header_style)
                    gcolidx += 1

        # Get a frame that will account for any duplicates in the column names.
        col_mapped_frame = self.df.loc[:, self.columns]

        # Write the body of the frame data series by series.
        for colidx in range(len(self.columns)):
            series = col_mapped_frame.iloc[:, colidx]
            for i, val in enumerate(series):
                yield ExcelCell(self.rowcounter + i, gcolidx + colidx, val)
