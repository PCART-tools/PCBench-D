    def _fit_strcols_to_terminal_width(self, strcols: list[list[str]]) -> str:
        from pandas import Series

        lines = self.adj.adjoin(1, *strcols).split("\n")
        max_len = Series(lines).str.len().max()
        # plus truncate dot col
        width, _ = get_terminal_size()
        dif = max_len - width
        # '+ 1' to avoid too wide repr (GH PR #17023)
        adj_dif = dif + 1
        col_lens = Series([Series(ele).apply(len).max() for ele in strcols])
        n_cols = len(col_lens)
        counter = 0
        while adj_dif > 0 and n_cols > 1:
            counter += 1
            mid = round(n_cols / 2)
            mid_ix = col_lens.index[mid]
            col_len = col_lens[mid_ix]
            # adjoin adds one
            adj_dif -= col_len + 1
            col_lens = col_lens.drop(mid_ix)
            n_cols = len(col_lens)

        # subtract index column
        max_cols_fitted = n_cols - self.fmt.index
        # GH-21180. Ensure that we print at least two.
        max_cols_fitted = max(max_cols_fitted, 2)
        self.fmt.max_cols_fitted = max_cols_fitted

        # Call again _truncate to cut frame appropriately
        # and then generate string representation
        self.fmt.truncate()
        strcols = self._get_strcols()
        return self.adj.adjoin(1, *strcols)
