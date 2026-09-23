    def _check_indexing_method(self, method):
        """
        Raise if we have a get_indexer `method` that is not supported or valid.
        """
        # GH#37871 for now this is only for IntervalIndex and CategoricalIndex
        if method is None:
            return

        if method in ["bfill", "backfill", "pad", "ffill", "nearest"]:
            raise NotImplementedError(
                f"method {method} not yet implemented for {type(self).__name__}"
            )

        raise ValueError("Invalid fill method")
