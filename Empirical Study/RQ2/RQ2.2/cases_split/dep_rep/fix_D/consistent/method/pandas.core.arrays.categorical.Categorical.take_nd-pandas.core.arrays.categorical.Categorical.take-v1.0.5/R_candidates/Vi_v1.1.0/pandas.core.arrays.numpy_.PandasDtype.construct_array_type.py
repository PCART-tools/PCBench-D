    @classmethod
    def construct_array_type(cls) -> Type["PandasArray"]:
        """
        Return the array type associated with this dtype.

        Returns
        -------
        type
        """
        return PandasArray
