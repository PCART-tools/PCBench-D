    def _format_col(self, i):
        frame = self.tr_frame
        formatter = self._get_formatter(i)
        return format_array(
            (frame.iloc[:, i]).get_values(),
            formatter, float_format=self.float_format, na_rep=self.na_rep,
            space=self.col_space
        )
