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
            # 'HTML output is disabled in QtConsole'
            return None

        if self._info_repr():
            buf = StringIO(u(""))
            self.info(buf=buf)
            # need to escape the <class>, should be the first line.
            val = buf.getvalue().replace('<', r'&lt;', 1).replace('>',
                                                                  r'&gt;', 1)
            return '<pre>' + val + '</pre>'

        if get_option("display.notebook_repr_html"):
            max_rows = get_option("display.max_rows")
            max_cols = get_option("display.max_columns")
            show_dimensions = get_option("display.show_dimensions")

            return ('<div style="max-height:1000px;'
                    'max-width:1500px;overflow:auto;">\n' +
                    self.to_html(max_rows=max_rows, max_cols=max_cols,
                                 show_dimensions=show_dimensions) + '\n</div>')
        else:
            return None
