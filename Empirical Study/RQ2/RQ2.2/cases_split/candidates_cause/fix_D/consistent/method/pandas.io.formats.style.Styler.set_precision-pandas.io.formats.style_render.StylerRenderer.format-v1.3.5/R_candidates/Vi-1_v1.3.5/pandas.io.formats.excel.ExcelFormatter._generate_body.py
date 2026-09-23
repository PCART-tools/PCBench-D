    def _generate_body(self, coloffset: int) -> Iterable[ExcelCell]:
        if self.styler is None:
            styles = None
        else:
            styles = self.styler._compute().ctx
            if not styles:
                styles = None
        xlstyle = None

        # Write the body of the frame data series by series.
        for colidx in range(len(self.columns)):
            series = self.df.iloc[:, colidx]
            for i, val in enumerate(series):
                if styles is not None:
                    css = ";".join(a + ":" + str(v) for (a, v) in styles[i, colidx])
                    xlstyle = self.style_converter(css)
                yield ExcelCell(self.rowcounter + i, colidx + coloffset, val, xlstyle)
