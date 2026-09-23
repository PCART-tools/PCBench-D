    def __unicode__(self):
        """
        Return a string representation for a particular DataFrame.

        Invoked by unicode(df) in py2 only. Yields a Unicode String in both
        py2/py3.
        """
        buf = StringIO(u(""))
        width, height = get_terminal_size()
        max_rows = (height if get_option("display.max_rows") == 0 else
                    get_option("display.max_rows"))
        show_dimensions = get_option("display.show_dimensions")

        self.to_string(buf=buf, name=self.name, dtype=self.dtype,
                       max_rows=max_rows, length=show_dimensions)
        result = buf.getvalue()

        return result
