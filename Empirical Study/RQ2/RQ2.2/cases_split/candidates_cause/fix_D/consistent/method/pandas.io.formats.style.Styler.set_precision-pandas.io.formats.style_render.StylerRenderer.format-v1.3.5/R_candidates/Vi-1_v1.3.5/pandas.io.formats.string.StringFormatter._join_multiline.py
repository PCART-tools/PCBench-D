    def _join_multiline(self, strcols_input: Iterable[list[str]]) -> str:
        lwidth = self.line_width
        adjoin_width = 1
        strcols = list(strcols_input)

        if self.fmt.index:
            idx = strcols.pop(0)
            # error: Argument 1 to "__call__" of "_NumberOp" has incompatible type
            # "None"; expected "Union[int, float, complex, number, bool_]"
            # error: Incompatible types in assignment (expression has type "number",
            # variable has type "Optional[int]")
            lwidth -= (  # type: ignore[assignment,arg-type]
                np.array([self.adj.len(x) for x in idx]).max() + adjoin_width
            )

        col_widths = [
            np.array([self.adj.len(x) for x in col]).max() if len(col) > 0 else 0
            for col in strcols
        ]

        assert lwidth is not None
        # error: Argument 1 to "_binify" has incompatible type "List[object]"; expected
        # "List[int]"
        col_bins = _binify(col_widths, lwidth)  # type: ignore[arg-type]
        nbins = len(col_bins)

        if self.fmt.is_truncated_vertically:
            assert self.fmt.max_rows_fitted is not None
            nrows = self.fmt.max_rows_fitted + 1
        else:
            nrows = len(self.frame)

        str_lst = []
        start = 0
        for i, end in enumerate(col_bins):
            row = strcols[start:end]
            if self.fmt.index:
                row.insert(0, idx)
            if nbins > 1:
                if end <= len(strcols) and i < nbins - 1:
                    row.append([" \\"] + ["  "] * (nrows - 1))
                else:
                    row.append([" "] * nrows)
            str_lst.append(self.adj.adjoin(adjoin_width, *row))
            start = end
        return "\n\n".join(str_lst)
