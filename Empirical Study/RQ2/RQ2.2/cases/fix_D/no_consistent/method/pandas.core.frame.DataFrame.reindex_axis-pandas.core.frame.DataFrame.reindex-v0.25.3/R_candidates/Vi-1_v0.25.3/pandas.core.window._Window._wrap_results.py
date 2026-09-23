    def _wrap_results(self, results, blocks, obj, exclude=None) -> FrameOrSeries:
        """
        Wrap the results.

        Parameters
        ----------
        results : list of ndarrays
        blocks : list of blocks
        obj : conformed data (may be resampled)
        exclude: list of columns to exclude, default to None
        """

        from pandas import Series, concat
        from pandas.core.index import ensure_index

        final = []
        for result, block in zip(results, blocks):

            result = self._wrap_result(result, block=block, obj=obj)
            if result.ndim == 1:
                return result
            final.append(result)

        # if we have an 'on' column
        # we want to put it back into the results
        # in the same location
        columns = self._selected_obj.columns
        if self.on is not None and not self._on.equals(obj.index):

            name = self._on.name
            final.append(Series(self._on, index=obj.index, name=name))

            if self._selection is not None:

                selection = ensure_index(self._selection)

                # need to reorder to include original location of
                # the on column (if its not already there)
                if name not in selection:
                    columns = self.obj.columns
                    indexer = columns.get_indexer(selection.tolist() + [name])
                    columns = columns.take(sorted(indexer))

        # exclude nuisance columns so that they are not reindexed
        if exclude is not None and exclude:
            columns = [c for c in columns if c not in exclude]

            if not columns:
                raise DataError("No numeric types to aggregate")

        if not len(final):
            return obj.astype("float64")
        return concat(final, axis=1).reindex(columns=columns, copy=False)
