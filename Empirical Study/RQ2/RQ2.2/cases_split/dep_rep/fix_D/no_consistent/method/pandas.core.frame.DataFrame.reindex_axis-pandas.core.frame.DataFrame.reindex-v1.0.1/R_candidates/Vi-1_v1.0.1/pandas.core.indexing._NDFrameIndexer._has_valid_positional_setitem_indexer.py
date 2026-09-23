    def _has_valid_positional_setitem_indexer(self, indexer) -> bool:
        """
        Validate that a positional indexer cannot enlarge its target
        will raise if needed, does not modify the indexer externally.

        Returns
        -------
        bool
        """
        if isinstance(indexer, dict):
            raise IndexError(f"{self.name} cannot enlarge its target object")
        else:
            if not isinstance(indexer, tuple):
                indexer = _tuplify(self.ndim, indexer)
            for ax, i in zip(self.obj.axes, indexer):
                if isinstance(i, slice):
                    # should check the stop slice?
                    pass
                elif is_list_like_indexer(i):
                    # should check the elements?
                    pass
                elif is_integer(i):
                    if i >= len(ax):
                        raise IndexError(
                            f"{self.name} cannot enlarge its target object"
                        )
                elif isinstance(i, dict):
                    raise IndexError(f"{self.name} cannot enlarge its target object")

        return True
