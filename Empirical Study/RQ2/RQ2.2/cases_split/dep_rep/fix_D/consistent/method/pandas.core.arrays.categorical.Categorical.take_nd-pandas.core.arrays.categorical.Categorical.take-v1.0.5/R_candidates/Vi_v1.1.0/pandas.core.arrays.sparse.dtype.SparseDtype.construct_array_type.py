    @classmethod
    def construct_array_type(cls) -> Type["SparseArray"]:
        """
        Return the array type associated with this dtype.

        Returns
        -------
        type
        """
        from pandas.core.arrays.sparse.array import SparseArray  # noqa: F811

        return SparseArray
