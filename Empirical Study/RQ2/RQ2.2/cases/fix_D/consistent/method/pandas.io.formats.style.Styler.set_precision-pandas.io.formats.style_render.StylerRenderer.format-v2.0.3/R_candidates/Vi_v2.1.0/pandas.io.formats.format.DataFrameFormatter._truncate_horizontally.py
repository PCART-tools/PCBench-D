    def _truncate_horizontally(self) -> None:
        """Remove columns, which are not to be displayed and adjust formatters.

        Attributes affected:
            - tr_frame
            - formatters
            - tr_col_num
        """
        assert self.max_cols_fitted is not None
        col_num = self.max_cols_fitted // 2
        if col_num >= 1:
            left = self.tr_frame.iloc[:, :col_num]
            right = self.tr_frame.iloc[:, -col_num:]
            self.tr_frame = concat((left, right), axis=1)

            # truncate formatter
            if isinstance(self.formatters, (list, tuple)):
                self.formatters = [
                    *self.formatters[:col_num],
                    *self.formatters[-col_num:],
                ]
        else:
            col_num = cast(int, self.max_cols)
            self.tr_frame = self.tr_frame.iloc[:, :col_num]
        self.tr_col_num = col_num
