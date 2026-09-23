    def _chk_truncate(self):
        from pandas.tools.merge import concat
        max_rows = self.max_rows
        truncate_v = max_rows and (len(self.series) > max_rows)
        series = self.series
        if truncate_v:
            if max_rows == 1:
                row_num = max_rows
                series = series.iloc[:max_rows]
            else:
                row_num = max_rows // 2
                series = concat((series.iloc[:row_num], series.iloc[-row_num:]))
            self.tr_row_num = row_num
        self.tr_series = series
        self.truncate_v = truncate_v
