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

        with com.temp_setattr(self, "as_index", True):
            # size already has the desired behavior in GH#49519, but this makes the
            # as_index=False path of _reindex_output fail on categorical groupers.
            result = self._reindex_output(result, fill_value=0)
        if not self.as_index:
            # error: Incompatible types in assignment (expression has
            # type "DataFrame", variable has type "Series")
            result = result.rename("size").reset_index()  # type: ignore[assignment]
        return result
