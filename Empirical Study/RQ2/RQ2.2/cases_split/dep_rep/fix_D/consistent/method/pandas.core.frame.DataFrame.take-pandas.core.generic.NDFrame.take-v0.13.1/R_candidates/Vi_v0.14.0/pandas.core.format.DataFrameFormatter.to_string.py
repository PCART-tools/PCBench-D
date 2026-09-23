    def to_string(self):
        """
        Render a DataFrame to a console-friendly tabular output.
        """

        frame = self.frame

        if len(frame.columns) == 0 or len(frame.index) == 0:
            info_line = (u('Empty %s\nColumns: %s\nIndex: %s')
                         % (type(self.frame).__name__,
                            com.pprint_thing(frame.columns),
                            com.pprint_thing(frame.index)))
            text = info_line
        else:
            strcols = self._to_str_columns()
            if self.line_width is None:
                text = adjoin(1, *strcols)
            else:
                text = self._join_multiline(*strcols)

        self.buf.writelines(text)

        if self.should_show_dimensions:
            self.buf.write("\n\n[%d rows x %d columns]"
                           % (len(frame), len(frame.columns)))
