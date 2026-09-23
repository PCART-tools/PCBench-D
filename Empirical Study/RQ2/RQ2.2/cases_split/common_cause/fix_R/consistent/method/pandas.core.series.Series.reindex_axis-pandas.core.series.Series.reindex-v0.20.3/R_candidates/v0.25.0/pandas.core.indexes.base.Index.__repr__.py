    def __repr__(self):
        """
        Return a string representation for this object.
        """
        klass = self.__class__.__name__
        data = self._format_data()
        attrs = self._format_attrs()
        space = self._format_space()

        prepr = (",%s" % space).join("%s=%s" % (k, v) for k, v in attrs)

        # no data provided, just attributes
        if data is None:
            data = ""

        res = "%s(%s%s)" % (klass, data, prepr)

        return res
