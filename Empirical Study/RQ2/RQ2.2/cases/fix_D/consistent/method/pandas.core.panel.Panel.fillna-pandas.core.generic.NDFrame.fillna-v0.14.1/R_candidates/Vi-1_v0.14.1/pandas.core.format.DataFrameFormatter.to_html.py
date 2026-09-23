    def to_html(self, classes=None):
        """
        Render a DataFrame to a html table.
        """
        html_renderer = HTMLFormatter(self, classes=classes,
                                      max_rows=self.max_rows,
                                      max_cols=self.max_cols)
        if hasattr(self.buf, 'write'):
            html_renderer.write_result(self.buf)
        elif isinstance(self.buf, compat.string_types):
            with open(self.buf, 'w') as f:
                html_renderer.write_result(f)
        else:
            raise TypeError('buf is not a file name and it has no write '
                            ' method')
