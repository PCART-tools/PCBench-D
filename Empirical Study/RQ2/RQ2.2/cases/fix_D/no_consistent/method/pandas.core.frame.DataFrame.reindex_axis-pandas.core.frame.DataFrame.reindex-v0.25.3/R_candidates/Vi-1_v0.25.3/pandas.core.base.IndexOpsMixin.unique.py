    def unique(self):
        values = self._values

        if hasattr(values, "unique"):

            result = values.unique()
        else:
            from pandas.core.algorithms import unique1d

            result = unique1d(values)

        return result
