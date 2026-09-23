    @final
    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def size(self) -> DataFrame | Series:
        """
        Compute group sizes.

        Returns
        -------
        DataFrame or Series
            Number of rows in each group as a Series if as_index is True
            or a DataFrame if as_index is False.
        """
        result = self.grouper.size()

        # GH28330 preserve subclassed Series/DataFrames through calls
        if isinstance(self.obj, Series):
            result = self._obj_1d_constructor(result, name=self.obj.name)
        else:
            result = self._obj_1d_constructor(result)

        if not self.as_index:
            # Item "None" of "Optional[Series]" has no attribute "reset_index"
            result = result.rename("size").reset_index()  # type: ignore[union-attr]

        return self._reindex_output(result, fill_value=0)
