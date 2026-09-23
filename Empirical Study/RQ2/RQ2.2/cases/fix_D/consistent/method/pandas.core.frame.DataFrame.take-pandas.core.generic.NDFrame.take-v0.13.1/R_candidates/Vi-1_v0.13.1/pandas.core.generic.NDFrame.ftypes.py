    @property
    def ftypes(self):
        """
        Return the ftypes (indication of sparse/dense and dtype)
        in this object.
        """
        from pandas import Series
        return Series(self._data.get_ftypes(),index=self._info_axis)
