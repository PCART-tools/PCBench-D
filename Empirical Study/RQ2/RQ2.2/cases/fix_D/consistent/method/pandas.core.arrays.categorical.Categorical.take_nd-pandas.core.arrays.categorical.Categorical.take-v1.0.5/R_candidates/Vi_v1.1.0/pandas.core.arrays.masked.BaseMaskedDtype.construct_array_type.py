    @classmethod
    def construct_array_type(cls) -> Type["BaseMaskedArray"]:
        """
        Return the array type associated with this dtype.

        Returns
        -------
        type
        """
        raise NotImplementedError
