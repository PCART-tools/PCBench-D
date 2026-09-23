    def sort_values(
        self,
        return_indexer: bool = False,
        ascending: bool = True,
        na_position: str = "last",
        key: Callable | None = None,
    ):
        sorted_index = self
        indexer = RangeIndex(range(len(self)))
        if key is not None:
            return super().sort_values(
                return_indexer=return_indexer,
                ascending=ascending,
                na_position=na_position,
                key=key,
            )
        else:
            sorted_index = self
            if ascending:
                if self.step < 0:
                    sorted_index = self[::-1]
                    indexer = indexer[::-1]
            else:
                if self.step > 0:
                    sorted_index = self[::-1]
                    indexer = indexer = indexer[::-1]

        if return_indexer:
            return sorted_index, indexer
        else:
            return sorted_index
