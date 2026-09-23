    @final
    def _should_partial_index(self, target: Index) -> bool:
        """
        Should we attempt partial-matching indexing?
        """
        if isinstance(self.dtype, IntervalDtype):
            if isinstance(target.dtype, IntervalDtype):
                return False
            # See https://github.com/pandas-dev/pandas/issues/47772 the commented
            # out code can be restored (instead of hardcoding `return True`)
            # once that issue is fixed
            # "Index" has no attribute "left"
            # return self.left._should_compare(target)  # type: ignore[attr-defined]
            return True
        return False
