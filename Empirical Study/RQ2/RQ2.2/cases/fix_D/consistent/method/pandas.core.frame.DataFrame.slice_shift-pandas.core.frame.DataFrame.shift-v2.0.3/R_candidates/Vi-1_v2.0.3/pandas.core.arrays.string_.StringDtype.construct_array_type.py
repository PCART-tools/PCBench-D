    def construct_array_type(  # type: ignore[override]
        self,
    ) -> type_t[BaseStringArray]:
        """
        Return the array type associated with this dtype.

        Returns
        -------
        type
        """
        from pandas.core.arrays.string_arrow import ArrowStringArray

        if self.storage == "python":
            return StringArray
        else:
            return ArrowStringArray
