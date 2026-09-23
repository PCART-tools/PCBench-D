    def to_string(self):
        """
        Render a DataFrame to a console-friendly tabular output.
        """
        from pandas import Series
        frame = self.frame

        if len(frame.columns) == 0 or len(frame.index) == 0:
            info_line = (u('Empty %s\nColumns: %s\nIndex: %s')
                         % (type(self.frame).__name__,
                            com.pprint_thing(frame.columns),
                            com.pprint_thing(frame.index)))
            text = info_line
        else:
            strcols = self._to_str_columns()
            if self.line_width is None:  # no need to wrap around just print the whole frame
                text = adjoin(1, *strcols)
            elif not isinstance(self.max_cols, int) or self.max_cols > 0:  # need to wrap around
                text = self._join_multiline(*strcols)
            else:  # max_cols == 0. Try to fit frame to terminal
                text = adjoin(1, *strcols).split('\n')
                row_lens = Series(text).apply(len)
                max_len_col_ix = np.argmax(row_lens)
                max_len = row_lens[max_len_col_ix]
                headers = [ele[0] for ele in strcols]
                # Size of last col determines dot col size. See `self._to_str_columns
                size_tr_col = len(headers[self.tr_size_col])
                max_len += size_tr_col  # Need to make space for largest row plus truncate dot col
                dif = max_len - self.w
                adj_dif = dif
                col_lens = Series([Series(ele).apply(len).max() for ele in strcols])
                n_cols = len(col_lens)
                counter = 0
                while adj_dif > 0 and n_cols > 1:
                    counter += 1
                    mid = int(round(n_cols / 2.))
                    mid_ix = col_lens.index[mid]
                    col_len = col_lens[mid_ix]
                    adj_dif -= (col_len + 1)  # adjoin adds one
                    col_lens = col_lens.drop(mid_ix)
                    n_cols = len(col_lens)
                max_cols_adj = n_cols - self.index  # subtract index column
                self.max_cols_adj = max_cols_adj

                # Call again _chk_truncate to cut frame appropriately
                # and then generate string representation
                self._chk_truncate()
                strcols = self._to_str_columns()
                text = adjoin(1, *strcols)

        self.buf.writelines(text)

        if self.should_show_dimensions:
            self.buf.write("\n\n[%d rows x %d columns]"
                           % (len(frame), len(frame.columns)))
