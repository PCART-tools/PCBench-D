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
                yield CssExcelCell(
                    row=self.rowcounter,
                    col=colindex + coloffset,
                    val=colname,
                    style=self.header_style,
                    css_styles=getattr(self.styler, "ctx_columns", None),
                    css_row=0,
                    css_col=colindex,
                    css_converter=self.style_converter,
                )
