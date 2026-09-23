    @final
    def _check_indexing_method(
        self,
        method: str_t | None,
        limit: int | None = None,
        tolerance=None,
    ) -> None:
        """
        Raise if we have a get_indexer `method` that is not supported or valid.
        """
        if method not in [None, "bfill", "backfill", "pad", "ffill", "nearest"]:
            # in practice the clean_reindex_fill_method call would raise
            #  before we get here
            raise ValueError("Invalid fill method")  # pragma: no cover

        if self._is_multi:
            if method == "nearest":
                raise NotImplementedError(
                    "method='nearest' not implemented yet "
                    "for MultiIndex; see GitHub issue 9365"
                )
            elif method == "pad" or method == "backfill":
                if tolerance is not None:
                    raise NotImplementedError(
                        "tolerance not implemented yet for MultiIndex"
                    )

        if is_interval_dtype(self.dtype) or is_categorical_dtype(self.dtype):
            # GH#37871 for now this is only for IntervalIndex and CategoricalIndex
            if method is not None:
                raise NotImplementedError(
                    f"method {method} not yet implemented for {type(self).__name__}"
                )

        if method is None:
            if tolerance is not None:
                raise ValueError(
                    "tolerance argument only valid if doing pad, "
                    "backfill or nearest reindexing"
                )
            if limit is not None:
                raise ValueError(
                    "limit argument only valid if doing pad, "
                    "backfill or nearest reindexing"
                )
