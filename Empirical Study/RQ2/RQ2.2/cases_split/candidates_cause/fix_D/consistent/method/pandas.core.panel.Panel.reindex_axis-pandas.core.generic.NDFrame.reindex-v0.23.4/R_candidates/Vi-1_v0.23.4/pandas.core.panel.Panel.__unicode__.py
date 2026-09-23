    def __unicode__(self):
        """
        Return a string representation for a particular Panel

        Invoked by unicode(df) in py2 only.
        Yields a Unicode String in both py2/py3.
        """

        class_name = str(self.__class__)

        dims = u('Dimensions: {dimensions}'.format(dimensions=' x '.join(
            ["{shape} ({axis})".format(shape=shape, axis=axis) for axis, shape
             in zip(self._AXIS_ORDERS, self.shape)])))

        def axis_pretty(a):
            v = getattr(self, a)
            if len(v) > 0:
                return u('{ax} axis: {x} to {y}'.format(ax=a.capitalize(),
                                                        x=pprint_thing(v[0]),
                                                        y=pprint_thing(v[-1])))
            else:
                return u('{ax} axis: None'.format(ax=a.capitalize()))

        output = '\n'.join(
            [class_name, dims] + [axis_pretty(a) for a in self._AXIS_ORDERS])
        return output
