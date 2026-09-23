    def __unicode__(self):
        """
        Return a string representation for this object.

        Invoked by unicode(df) in py2 only. Yields a Unicode String in both
        py2/py3.
        """
        klass = self.__class__.__name__
        data = self._format_data()
        attrs = self._format_attrs()
        space = self._format_space()

        prepr = (u(",%s") %
                 space).join(u("%s=%s") % (k, v) for k, v in attrs)

        # no data provided, just attributes
        if data is None:
            data = ''

        res = u("%s(%s%s)") % (klass, data, prepr)

        return res
