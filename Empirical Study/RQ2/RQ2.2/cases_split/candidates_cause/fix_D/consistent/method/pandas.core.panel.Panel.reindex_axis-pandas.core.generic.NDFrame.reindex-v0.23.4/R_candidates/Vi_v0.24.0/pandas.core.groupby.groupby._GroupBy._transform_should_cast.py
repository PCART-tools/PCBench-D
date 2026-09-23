    def _transform_should_cast(self, func_nm):
        """
        Parameters:
        -----------
        func_nm: str
            The name of the aggregation function being performed

        Returns:
        --------
        bool
            Whether transform should attempt to cast the result of aggregation
        """
        return (self.size().fillna(0) > 0).any() and (
            func_nm not in base.cython_cast_blacklist)
