    def _repr_html_(self):
        """
        Return a html representation for a particular DataFrame.
        Mainly for IPython notebook.
        """
        # ipnb in html repr mode allows scrolling
        # users strongly prefer to h-scroll a wide HTML table in the browser
        # then to get a summary view. GH3541, GH3573
        ipnbh = com.in_ipnb() and get_option('display.notebook_repr_html')

        # qtconsole doesn't report it's line width, and also
        # behaves badly when outputting an HTML table
        # that doesn't fit the window, so disable it.
        if com.in_qtconsole():
            raise ValueError('Disable HTML output in QtConsole')

        if self._info_repr():
            buf = StringIO(u(""))
            self.info(buf=buf)
            return '<pre>' + buf.getvalue() + '</pre>'

        if get_option("display.notebook_repr_html"):
            max_rows = get_option("display.max_rows")
            max_cols = get_option("display.max_columns")

            return ('<div style="max-height:1000px;'
                    'max-width:1500px;overflow:auto;">\n' +
                    self.to_html(max_rows=max_rows, max_cols=max_cols,
                                 show_dimensions=True) + '\n</div>')
        else:
            return None
