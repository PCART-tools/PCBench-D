    def value_counts(self, dropna=False):
        """
        Return a Series containing counts of unique values.

        Parameters
        ----------
        dropna : boolean, default True
            Don't include counts of NaT values.

        Returns
        -------
        Series
        """
        from pandas import Series, Index

        if dropna:
            values = self[~self.isna()]._data
        else:
            values = self._data

        cls = type(self)

        result = value_counts(values, sort=False, dropna=dropna)
        index = Index(
            cls(result.index.view("i8"), dtype=self.dtype), name=result.index.name
        )
        return Series(result.values, index=index, name=result.name)
