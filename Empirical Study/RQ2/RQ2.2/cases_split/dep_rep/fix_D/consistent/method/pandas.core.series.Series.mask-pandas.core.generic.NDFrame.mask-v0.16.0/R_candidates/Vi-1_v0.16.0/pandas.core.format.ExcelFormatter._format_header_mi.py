    def _format_header_mi(self):
        has_aliases = isinstance(self.header, (tuple, list, np.ndarray, Index))
        if not(has_aliases or self.header):
            return

        columns = self.columns
        level_strs = columns.format(sparsify=True, adjoin=False, names=False)
        level_lengths = _get_level_lengths(level_strs)
        coloffset = 0
        lnum = 0

        if self.index and isinstance(self.df.index, MultiIndex):
            coloffset = len(self.df.index[0]) - 1

        if self.merge_cells:
            # Format multi-index as a merged cells.
            for lnum in range(len(level_lengths)):
                name = columns.names[lnum]
                yield ExcelCell(lnum, coloffset, name, header_style)

            for lnum, (spans, levels, labels) in enumerate(zip(level_lengths,
                                                               columns.levels,
                                                               columns.labels)
                                                           ):
                values = levels.take(labels)
                for i in spans:
                    if spans[i] > 1:
                        yield ExcelCell(lnum,
                                        coloffset + i + 1,
                                        values[i],
                                        header_style,
                                        lnum,
                                        coloffset + i + spans[i])
                    else:
                        yield ExcelCell(lnum,
                                        coloffset + i + 1,
                                        values[i],
                                        header_style)
        else:
            # Format in legacy format with dots to indicate levels.
            for i, values in enumerate(zip(*level_strs)):
                v = ".".join(map(com.pprint_thing, values))
                yield ExcelCell(lnum, coloffset + i + 1, v, header_style)

        self.rowcounter = lnum
