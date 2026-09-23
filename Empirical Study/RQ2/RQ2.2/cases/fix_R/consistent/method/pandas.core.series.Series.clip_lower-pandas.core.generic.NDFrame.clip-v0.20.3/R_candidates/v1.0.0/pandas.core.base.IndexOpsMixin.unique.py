    def unique(self):
        values = self._values

        if hasattr(values, "unique"):

            result = values.unique()
        else:
            result = unique1d(values)

        return result
