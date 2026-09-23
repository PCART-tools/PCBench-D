    @Appender(DataFrame.count.__doc__)
    def count(self, axis=0, **kwds):
        if axis is None:
            axis = self._stat_axis_number

        return self.apply(lambda x: x.count(), axis=axis)
