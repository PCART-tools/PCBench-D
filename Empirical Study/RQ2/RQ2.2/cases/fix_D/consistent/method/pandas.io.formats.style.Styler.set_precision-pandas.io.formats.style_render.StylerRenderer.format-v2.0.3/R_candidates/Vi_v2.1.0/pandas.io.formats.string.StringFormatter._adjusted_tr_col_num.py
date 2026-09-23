    @property
    def _adjusted_tr_col_num(self) -> int:
        return self.fmt.tr_col_num + 1 if self.fmt.index else self.fmt.tr_col_num
