    @final
    def _should_partial_index(self, target: Index) -> bool:
        """
        Should we attempt partial-matching indexing?
        """
        if is_interval_dtype(self.dtype):
            # "Index" has no attribute "left"
            return self.left._should_compare(target)  # type: ignore[attr-defined]
        return False
