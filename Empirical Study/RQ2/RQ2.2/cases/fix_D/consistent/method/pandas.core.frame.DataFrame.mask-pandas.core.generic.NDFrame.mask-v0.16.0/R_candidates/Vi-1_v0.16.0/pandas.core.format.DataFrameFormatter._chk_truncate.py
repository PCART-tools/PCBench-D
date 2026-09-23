    def _chk_truncate(self):
        '''
        Checks whether the frame should be truncated. If so, slices
        the frame up.
        '''
        from pandas.tools.merge import concat

        # Column of which first element is used to determine width of a dot col
        self.tr_size_col = -1

        # Cut the data to the information actually printed
        max_cols = self.max_cols
        max_rows = self.max_rows

        if max_cols == 0 or max_rows == 0:  # assume we are in the terminal (why else = 0)
            (w, h) = get_terminal_size()
            self.w = w
            self.h = h
            if self.max_rows == 0:
                dot_row = 1
                prompt_row = 1
                if self.show_dimensions:
                    show_dimension_rows = 3
                n_add_rows = self.header + dot_row + show_dimension_rows + prompt_row
                max_rows_adj = self.h - n_add_rows  # rows available to fill with actual data
                self.max_rows_adj = max_rows_adj

            # Format only rows and columns that could potentially fit the screen
            if max_cols == 0 and len(self.frame.columns) > w:
                max_cols = w
            if max_rows == 0 and len(self.frame) > h:
                max_rows = h

        if not hasattr(self, 'max_rows_adj'):
            self.max_rows_adj = max_rows
        if not hasattr(self, 'max_cols_adj'):
            self.max_cols_adj = max_cols

        max_cols_adj = self.max_cols_adj
        max_rows_adj = self.max_rows_adj

        truncate_h = max_cols_adj and (len(self.columns) > max_cols_adj)
        truncate_v = max_rows_adj and (len(self.frame) > max_rows_adj)

        frame = self.frame
        if truncate_h:
            if max_cols_adj == 0:
                col_num = len(frame.columns)
            elif max_cols_adj == 1:
                frame = frame.iloc[:, :max_cols]
                col_num = max_cols
            else:
                col_num = (max_cols_adj // 2)
                frame = concat((frame.iloc[:, :col_num], frame.iloc[:, -col_num:]), axis=1)
            self.tr_col_num = col_num
        if truncate_v:
            if max_rows_adj == 0:
                row_num = len(frame)
            if max_rows_adj == 1:
                row_num = max_rows
                frame = frame.iloc[:max_rows, :]
            else:
                row_num = max_rows_adj // 2
                frame = concat((frame.iloc[:row_num, :], frame.iloc[-row_num:, :]))
            self.tr_row_num = row_num

        self.tr_frame = frame
        self.truncate_h = truncate_h
        self.truncate_v = truncate_v
        self.is_truncated = self.truncate_h or self.truncate_v
