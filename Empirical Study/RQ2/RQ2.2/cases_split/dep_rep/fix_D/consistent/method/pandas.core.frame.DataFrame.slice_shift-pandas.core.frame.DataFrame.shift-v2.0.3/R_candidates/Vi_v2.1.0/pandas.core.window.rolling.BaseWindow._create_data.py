    def _create_data(self, obj: NDFrameT, numeric_only: bool = False) -> NDFrameT:
        """
        Split data into blocks & return conformed data.
        """
        # filter out the on from the object
        if self.on is not None and not isinstance(self.on, Index) and obj.ndim == 2:
            obj = obj.reindex(columns=obj.columns.difference([self.on]), copy=False)
        if obj.ndim > 1 and (numeric_only or self.axis == 1):
            # GH: 20649 in case of mixed dtype and axis=1 we have to convert everything
            # to float to calculate the complete row at once. We exclude all non-numeric
            # dtypes.
            obj = self._make_numeric_only(obj)
        if self.axis == 1:
            obj = obj.astype("float64", copy=False)
            obj._mgr = obj._mgr.consolidate()
        return obj
