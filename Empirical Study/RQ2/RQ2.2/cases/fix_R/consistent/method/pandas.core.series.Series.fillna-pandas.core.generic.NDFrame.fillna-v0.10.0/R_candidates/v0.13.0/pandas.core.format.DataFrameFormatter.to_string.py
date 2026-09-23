    def to_string(self, force_unicode=None):
        """
        Render a DataFrame to a console-friendly tabular output.
        """
        import warnings
        if force_unicode is not None:  # pragma: no cover
            warnings.warn(
                "force_unicode is deprecated, it will have no effect",
                FutureWarning)

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

        if self.show_dimensions:
            self.buf.write("\n\n[%d rows x %d columns]"
                           % (len(frame), len(frame.columns)))
