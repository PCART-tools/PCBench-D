    @classmethod
    def construct_array_type(cls) -> type_t[PandasArray]:
        """
        Return the array type associated with this dtype.

        Returns
        -------
        type
        """
        from pandas.core.arrays import PandasArray

        return PandasArray
