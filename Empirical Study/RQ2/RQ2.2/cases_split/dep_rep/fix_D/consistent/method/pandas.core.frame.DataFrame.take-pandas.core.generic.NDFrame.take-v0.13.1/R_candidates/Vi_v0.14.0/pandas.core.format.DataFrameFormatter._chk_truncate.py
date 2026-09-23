    def _chk_truncate(self):
        from pandas.tools.merge import concat

        truncate_h = self.max_cols and (len(self.columns) > self.max_cols)
        truncate_v = self.max_rows and (len(self.frame) > self.max_rows)

        # Cut the data to the information actually printed
        max_cols = self.max_cols
        max_rows = self.max_rows
        frame = self.frame
        if truncate_h:
            if max_cols > 1:
                col_num = (max_cols // 2)
                frame = concat( (frame.iloc[:,:col_num],frame.iloc[:,-col_num:]),axis=1 )
            else:
                col_num = max_cols
                frame = frame.iloc[:,:max_cols]
            self.tr_col_num = col_num
        if truncate_v:
            if max_rows > 1:
                row_num = max_rows // 2
                frame = concat( (frame.iloc[:row_num,:],frame.iloc[-row_num:,:]) )
            else:
                row_num = max_rows
                frame = frame.iloc[:max_rows,:]
            self.tr_row_num = row_num

        self.tr_frame = frame
        self.truncate_h = truncate_h
        self.truncate_v = truncate_v
        self.is_truncated = self.truncate_h or self.truncate_v
