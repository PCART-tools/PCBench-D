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
                    mergestart, mergeend = None, None
                    if span_val > 1:
                        mergestart, mergeend = lnum, coloffset + i + span_val
                    yield CssExcelCell(
                        row=lnum,
                        col=coloffset + i + 1,
                        val=values[i],
                        style=self.header_style,
                        css_styles=getattr(self.styler, "ctx_columns", None),
                        css_row=lnum,
                        css_col=i,
                        css_converter=self.style_converter,
                        mergestart=mergestart,
                        mergeend=mergeend,
                    )
        else:
            # Format in legacy format with dots to indicate levels.
            for i, values in enumerate(zip(*level_strs)):
                v = ".".join(map(pprint_thing, values))
                yield CssExcelCell(
                    row=lnum,
                    col=coloffset + i + 1,
                    val=v,
                    style=self.header_style,
                    css_styles=getattr(self.styler, "ctx_columns", None),
                    css_row=lnum,
                    css_col=i,
                    css_converter=self.style_converter,
                )

        self.rowcounter = lnum
