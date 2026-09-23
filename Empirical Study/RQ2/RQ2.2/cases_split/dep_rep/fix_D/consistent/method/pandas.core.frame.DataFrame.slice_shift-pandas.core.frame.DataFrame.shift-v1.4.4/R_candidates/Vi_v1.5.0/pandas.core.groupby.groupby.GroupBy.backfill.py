    def backfill(self, limit=None):
        warnings.warn(
            "backfill is deprecated and will be removed in a future version. "
            "Use bfill instead.",
            FutureWarning,
            stacklevel=find_stack_level(inspect.currentframe()),
        )
        return self.bfill(limit=limit)
