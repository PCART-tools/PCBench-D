    def _repr_html_(self):
        """
        Return a html representation for a particular DataFrame.

        Mainly for IPython notebook.
        """
        if self._info_repr():
            buf = StringIO("")
            self.info(buf=buf)
            # need to escape the <class>, should be the first line.
            val = buf.getvalue().replace("<", r"&lt;", 1)
            val = val.replace(">", r"&gt;", 1)
            return "<pre>" + val + "</pre>"

        if get_option("display.notebook_repr_html"):
            max_rows = get_option("display.max_rows")
            max_cols = get_option("display.max_columns")
            show_dimensions = get_option("display.show_dimensions")

            return self.to_html(
                max_rows=max_rows,
                max_cols=max_cols,
                show_dimensions=show_dimensions,
                notebook=True,
            )
        else:
            return None
