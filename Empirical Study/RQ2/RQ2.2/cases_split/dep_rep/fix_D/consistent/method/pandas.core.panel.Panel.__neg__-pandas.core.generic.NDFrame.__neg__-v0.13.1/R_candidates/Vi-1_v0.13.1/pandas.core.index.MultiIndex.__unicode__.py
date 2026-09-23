    def __unicode__(self):
        """
        Return a string representation for a particular Index

        Invoked by unicode(df) in py2 only. Yields a Unicode String in both
        py2/py3.
        """
        rows = self.format(names=True)
        max_rows = get_option('display.max_rows')
        if len(rows) > max_rows:
            spaces = (len(rows[0]) - 3) // 2
            centered = ' ' * spaces
            half = max_rows // 2
            rows = rows[:half] + [centered + '...' + centered] + rows[-half:]
        return "\n".join(rows)
