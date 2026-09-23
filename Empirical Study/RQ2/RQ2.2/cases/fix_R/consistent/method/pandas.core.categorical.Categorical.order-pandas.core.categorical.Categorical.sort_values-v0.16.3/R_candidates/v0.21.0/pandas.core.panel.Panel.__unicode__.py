    def __unicode__(self):
        """
        Return a string representation for a particular Panel

        Invoked by unicode(df) in py2 only.
        Yields a Unicode String in both py2/py3.
        """

        class_name = str(self.__class__)

        shape = self.shape
        dims = u('Dimensions: %s') % ' x '.join(
            ["%d (%s)" % (s, a) for a, s in zip(self._AXIS_ORDERS, shape)])

        def axis_pretty(a):
            v = getattr(self, a)
            if len(v) > 0:
                return u('%s axis: %s to %s') % (a.capitalize(),
                                                 pprint_thing(v[0]),
                                                 pprint_thing(v[-1]))
            else:
                return u('%s axis: None') % a.capitalize()

        output = '\n'.join(
            [class_name, dims] + [axis_pretty(a) for a in self._AXIS_ORDERS])
        return output
