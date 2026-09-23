    def _gotitem(self, key, ndim, subset=None):
        """
        sub-classes to define
        return a sliced object

        Parameters
        ----------
        key : string / list of selections
        ndim : 1,2
            requested ndim of result
        subset : object, default None
            subset to act on
        """

        if ndim == 2:
            if subset is None:
                subset = self.obj
            return DataFrameGroupBy(subset, self.grouper, selection=key,
                                    grouper=self.grouper,
                                    exclusions=self.exclusions,
                                    as_index=self.as_index)
        elif ndim == 1:
            if subset is None:
                subset = self.obj[key]
            return SeriesGroupBy(subset, selection=key,
                                 grouper=self.grouper)

        raise AssertionError("invalid ndim for _gotitem")
