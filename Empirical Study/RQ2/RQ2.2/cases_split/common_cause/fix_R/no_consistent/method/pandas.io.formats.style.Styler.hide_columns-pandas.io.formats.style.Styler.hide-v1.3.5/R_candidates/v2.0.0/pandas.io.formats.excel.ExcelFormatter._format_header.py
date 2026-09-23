    def _format_header(self) -> Iterable[ExcelCell]:
        gen: Iterable[ExcelCell]

        if isinstance(self.columns, MultiIndex):
            gen = self._format_header_mi()
        else:
            gen = self._format_header_regular()

        gen2: Iterable[ExcelCell] = ()

        if self.df.index.names:
            row = [x if x is not None else "" for x in self.df.index.names] + [
                ""
            ] * len(self.columns)
            if reduce(lambda x, y: x and y, map(lambda x: x != "", row)):
                gen2 = (
                    ExcelCell(self.rowcounter, colindex, val, self.header_style)
                    for colindex, val in enumerate(row)
                )
                self.rowcounter += 1
        return itertools.chain(gen, gen2)
