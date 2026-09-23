    def _insert_dot_separator_horizontal(
        self, strcols: list[list[str]], index_length: int
    ) -> list[list[str]]:
        strcols.insert(self._adjusted_tr_col_num, [" ..."] * index_length)
        return strcols
