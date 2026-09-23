    def _append(
        self,
        other,
        ignore_index: bool = False,
        verify_integrity: bool = False,
        sort: bool = False,
    ) -> DataFrame:
        combined_columns = None
        if isinstance(other, (Series, dict)):
            if isinstance(other, dict):
                if not ignore_index:
                    raise TypeError("Can only append a dict if ignore_index=True")
                other = Series(other)
            if other.name is None and not ignore_index:
                raise TypeError(
                    "Can only append a Series if ignore_index=True "
                    "or if the Series has a name"
                )

            index = Index([other.name], name=self.index.name)
            idx_diff = other.index.difference(self.columns)
            combined_columns = self.columns.append(idx_diff)
            row_df = other.to_frame().T
            # infer_objects is needed for
            #  test_append_empty_frame_to_series_with_dateutil_tz
            other = row_df.infer_objects().rename_axis(index.names, copy=False)
        elif isinstance(other, list):
            if not other:
                pass
            elif not isinstance(other[0], DataFrame):
                other = DataFrame(other)
                if self.index.name is not None and not ignore_index:
                    other.index.name = self.index.name

        from pandas.core.reshape.concat import concat

        if isinstance(other, (list, tuple)):
            to_concat = [self, *other]
        else:
            to_concat = [self, other]

        result = concat(
            to_concat,
            ignore_index=ignore_index,
            verify_integrity=verify_integrity,
            sort=sort,
        )
        if (
            combined_columns is not None
            and not sort
            and not combined_columns.equals(result.columns)
        ):
            # TODO: reindexing here is a kludge bc union_indexes does not
            #  pass sort to index.union, xref #43375
            # combined_columns.equals check is necessary for preserving dtype
            #  in test_crosstab_normalize
            result = result.reindex(combined_columns, axis=1)
        return result.__finalize__(self, method="append")
