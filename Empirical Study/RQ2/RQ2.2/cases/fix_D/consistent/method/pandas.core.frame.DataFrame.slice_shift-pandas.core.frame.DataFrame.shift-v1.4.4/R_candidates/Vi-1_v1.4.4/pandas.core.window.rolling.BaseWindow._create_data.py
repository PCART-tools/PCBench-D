    def _create_data(self, obj: NDFrameT) -> NDFrameT:
        """
        Split data into blocks & return conformed data.
        """
        # filter out the on from the object
        if self.on is not None and not isinstance(self.on, Index) and obj.ndim == 2:
            obj = obj.reindex(columns=obj.columns.difference([self.on]), copy=False)
        if self.axis == 1:
            # GH: 20649 in case of mixed dtype and axis=1 we have to convert everything
            # to float to calculate the complete row at once. We exclude all non-numeric
            # dtypes.
            obj = obj.select_dtypes(include=["number"], exclude=["timedelta"])
            obj = obj.astype("float64", copy=False)
            obj._mgr = obj._mgr.consolidate()
        return obj
