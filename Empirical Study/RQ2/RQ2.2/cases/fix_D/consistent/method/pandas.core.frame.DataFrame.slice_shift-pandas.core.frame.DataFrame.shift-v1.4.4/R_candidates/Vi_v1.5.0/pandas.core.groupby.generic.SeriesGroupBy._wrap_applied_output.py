    def _wrap_applied_output(
        self,
        data: Series,
        values: list[Any],
        not_indexed_same: bool = False,
        override_group_keys: bool = False,
    ) -> DataFrame | Series:
        """
        Wrap the output of SeriesGroupBy.apply into the expected result.

        Parameters
        ----------
        data : Series
            Input data for groupby operation.
        values : List[Any]
            Applied output for each group.
        not_indexed_same : bool, default False
            Whether the applied outputs are not indexed the same as the group axes.

        Returns
        -------
        DataFrame or Series
        """
        if len(values) == 0:
            # GH #6265
            return self.obj._constructor(
                [],
                name=self.obj.name,
                index=self.grouper.result_index,
                dtype=data.dtype,
            )
        assert values is not None

        if isinstance(values[0], dict):
            # GH #823 #24880
            index = self.grouper.result_index
            res_df = self.obj._constructor_expanddim(values, index=index)
            res_df = self._reindex_output(res_df)
            # if self.observed is False,
            # keep all-NaN rows created while re-indexing
            res_ser = res_df.stack(dropna=self.observed)
            res_ser.name = self.obj.name
            return res_ser
        elif isinstance(values[0], (Series, DataFrame)):
            result = self._concat_objects(
                values,
                not_indexed_same=not_indexed_same,
                override_group_keys=override_group_keys,
            )
            result.name = self.obj.name
            return result
        else:
            # GH #6265 #24880
            result = self.obj._constructor(
                data=values, index=self.grouper.result_index, name=self.obj.name
            )
            return self._reindex_output(result)
