    def fillna(self, fill_value=None, method=None, limit=None):
        """ Fill NA/NaN values using the specified method.

        Parameters
        ----------
        method : {'backfill', 'bfill', 'pad', 'ffill', None}, default None
            Method to use for filling holes in reindexed Series
            pad / ffill: propagate last valid observation forward to next valid
            backfill / bfill: use NEXT valid observation to fill gap
        value : scalar
            Value to use to fill holes (e.g. 0)
        limit : int, default None
            Maximum size gap to forward or backward fill (not implemented yet!)

        Returns
        -------
        filled : Categorical with NA/NaN filled
        """

        if fill_value is None:
            fill_value = np.nan
        if limit is not None:
            raise NotImplementedError

        values = self._codes

        # Make sure that we also get NA in categories
        if self.categories.dtype.kind in ['S', 'O', 'f']:
            if np.nan in self.categories:
                values = values.copy()
                nan_pos = np.where(isnull(self.categories))[0]
                # we only have one NA in categories
                values[values == nan_pos] = -1


        # pad / bfill
        if method is not None:

            values = self.to_dense().reshape(-1,len(self))
            values = com.interpolate_2d(
                values, method, 0, None, fill_value).astype(self.categories.dtype)[0]
            values = _get_codes_for_values(values, self.categories)

        else:

            if not isnull(fill_value) and fill_value not in self.categories:
                raise ValueError("fill value must be in categories")

            mask = values==-1
            if mask.any():
                values = values.copy()
                values[mask] = self.categories.get_loc(fill_value)

        return Categorical(values, categories=self.categories, ordered=self.ordered,
                           name=self.name, fastpath=True)
