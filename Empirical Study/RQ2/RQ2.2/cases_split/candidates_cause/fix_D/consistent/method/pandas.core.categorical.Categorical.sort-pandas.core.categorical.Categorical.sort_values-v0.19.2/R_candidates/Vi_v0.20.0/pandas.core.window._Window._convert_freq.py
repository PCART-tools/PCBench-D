    def _convert_freq(self, how=None):
        """ resample according to the how, return a new object """

        obj = self._selected_obj
        index = None
        if (self.freq is not None and
                isinstance(obj, (ABCSeries, ABCDataFrame))):
            if how is not None:
                warnings.warn("The how kw argument is deprecated and removed "
                              "in a future version. You can resample prior "
                              "to passing to a window function", FutureWarning,
                              stacklevel=6)

            obj = obj.resample(self.freq).aggregate(how or 'asfreq')

        return obj, index
