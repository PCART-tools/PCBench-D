    def _format_col(self, i):
        formatter = self._get_formatter(i)
        return format_array(
            (self.frame.iloc[:self.max_rows_displayed, i]).get_values(),
            formatter, float_format=self.float_format, na_rep=self.na_rep,
            space=self.col_space
        )
