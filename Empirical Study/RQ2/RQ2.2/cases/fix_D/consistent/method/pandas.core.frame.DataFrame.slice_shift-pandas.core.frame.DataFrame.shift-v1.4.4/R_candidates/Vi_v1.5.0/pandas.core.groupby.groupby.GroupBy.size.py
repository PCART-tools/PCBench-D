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

        if self.axis == 1:
            return DataFrame(
                data=np.tile(result.values, (self.obj.shape[0], 1)),
                columns=result.index,
                index=self.obj.index,
            )

        # GH28330 preserve subclassed Series/DataFrames through calls
        if isinstance(self.obj, Series):
            result = self._obj_1d_constructor(result, name=self.obj.name)
        else:
            result = self._obj_1d_constructor(result)

        if not self.as_index:
            # error: Incompatible types in assignment (expression has
            # type "DataFrame", variable has type "Series")
            result = result.rename("size").reset_index()  # type: ignore[assignment]

        return self._reindex_output(result, fill_value=0)
