    @property
    def dtypes(self):
        """Return the dtypes in this object."""
        from pandas import Series
        return Series(self._data.get_dtypes(), index=self._info_axis,
                      dtype=np.object_)
