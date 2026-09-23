    def _format_header_mi(self) -> Iterable[ExcelCell]:
        if self.columns.nlevels > 1:
            if not self.index:
                raise NotImplementedError(
                    "Writing to Excel with MultiIndex columns and no "
                    "index ('index'=False) is not yet implemented."
                )

        if not (self._has_aliases or self.header):
            return

        columns = self.columns
        level_strs = columns.format(
            sparsify=self.merge_cells, adjoin=False, names=False
        )
        level_lengths = get_level_lengths(level_strs)
        coloffset = 0
        lnum = 0

        if self.index and isinstance(self.df.index, MultiIndex):
            coloffset = len(self.df.index[0]) - 1

        if self.merge_cells:
            # Format multi-index as a merged cells.
            for lnum, name in enumerate(columns.names):
                yield ExcelCell(
                    row=lnum,
                    col=coloffset,
                    val=name,
                    style=self.header_style,
                )

            for lnum, (spans, levels, level_codes) in enumerate(
                zip(level_lengths, columns.levels, columns.codes)
            ):
                values = levels.take(level_codes)
                for i, span_val in spans.items():
                    spans_multiple_cells = span_val > 1
                    yield ExcelCell(
                        row=lnum,
                        col=coloffset + i + 1,
                        val=values[i],
                        style=self.header_style,
                        mergestart=lnum if spans_multiple_cells else None,
                        mergeend=(
                            coloffset + i + span_val if spans_multiple_cells else None
                        ),
                    )
        else:
            # Format in legacy format with dots to indicate levels.
            for i, values in enumerate(zip(*level_strs)):
                v = ".".join(map(pprint_thing, values))
                yield ExcelCell(lnum, coloffset + i + 1, v, self.header_style)

        self.rowcounter = lnum
