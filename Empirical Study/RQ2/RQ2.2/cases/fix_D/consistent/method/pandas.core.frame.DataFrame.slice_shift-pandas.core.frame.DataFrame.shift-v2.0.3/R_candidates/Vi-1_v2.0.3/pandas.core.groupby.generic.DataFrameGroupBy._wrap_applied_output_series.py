    def _wrap_applied_output_series(
        self,
        values: list[Series],
        not_indexed_same: bool,
        first_not_none,
        key_index: Index | None,
        is_transform: bool,
    ) -> DataFrame | Series:
        kwargs = first_not_none._construct_axes_dict()
        backup = Series(**kwargs)
        values = [x if (x is not None) else backup for x in values]

        all_indexed_same = all_indexes_same(x.index for x in values)

        if not all_indexed_same:
            # GH 8467
            return self._concat_objects(
                values,
                not_indexed_same=True,
                is_transform=is_transform,
            )

        # Combine values
        # vstack+constructor is faster than concat and handles MI-columns
        stacked_values = np.vstack([np.asarray(v) for v in values])

        if self.axis == 0:
            index = key_index
            columns = first_not_none.index.copy()
            if columns.name is None:
                # GH6124 - propagate name of Series when it's consistent
                names = {v.name for v in values}
                if len(names) == 1:
                    columns.name = list(names)[0]
        else:
            index = first_not_none.index
            columns = key_index
            stacked_values = stacked_values.T

        if stacked_values.dtype == object:
            # We'll have the DataFrame constructor do inference
            stacked_values = stacked_values.tolist()
        result = self.obj._constructor(stacked_values, index=index, columns=columns)

        if not self.as_index:
            result = self._insert_inaxis_grouper(result)

        return self._reindex_output(result)
