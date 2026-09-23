    def _render(
        self,
        sparse_index: bool,
        sparse_columns: bool,
        max_rows: int | None = None,
        max_cols: int | None = None,
        blank: str = "",
    ):
        """
        Computes and applies styles and then generates the general render dicts.

        Also extends the `ctx` and `ctx_index` attributes with those of concatenated
        stylers for use within `_translate_latex`
        """
        self._compute()
        dxs = []
        ctx_len = len(self.index)
        for i, concatenated in enumerate(self.concatenated):
            concatenated.hide_index_ = self.hide_index_
            concatenated.hidden_columns = self.hidden_columns
            foot = f"{self.css['foot']}{i}"
            concatenated.css = {
                **self.css,
                "data": f"{foot}_data",
                "row_heading": f"{foot}_row_heading",
                "row": f"{foot}_row",
                "foot": f"{foot}_foot",
            }
            dx = concatenated._render(
                sparse_index, sparse_columns, max_rows, max_cols, blank
            )
            dxs.append(dx)

            for (r, c), v in concatenated.ctx.items():
                self.ctx[(r + ctx_len, c)] = v
            for (r, c), v in concatenated.ctx_index.items():
                self.ctx_index[(r + ctx_len, c)] = v

            ctx_len += len(concatenated.index)

        d = self._translate(
            sparse_index, sparse_columns, max_rows, max_cols, blank, dxs
        )
        return d
