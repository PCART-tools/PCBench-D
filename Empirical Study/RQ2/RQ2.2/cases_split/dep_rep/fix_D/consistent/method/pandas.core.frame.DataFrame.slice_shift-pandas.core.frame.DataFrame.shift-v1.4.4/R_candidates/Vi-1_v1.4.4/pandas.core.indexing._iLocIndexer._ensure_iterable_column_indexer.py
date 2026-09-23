    def _ensure_iterable_column_indexer(self, column_indexer):
        """
        Ensure that our column indexer is something that can be iterated over.
        """
        ilocs: Sequence[int]
        if is_integer(column_indexer):
            ilocs = [column_indexer]
        elif isinstance(column_indexer, slice):
            ilocs = np.arange(len(self.obj.columns))[  # type: ignore[assignment]
                column_indexer
            ]
        elif isinstance(column_indexer, np.ndarray) and is_bool_dtype(
            column_indexer.dtype
        ):
            ilocs = np.arange(len(column_indexer))[column_indexer]
        else:
            ilocs = column_indexer
        return ilocs
