    def pad(self, limit=None):
        warnings.warn(
            "pad is deprecated and will be removed in a future version. "
            "Use ffill instead.",
            FutureWarning,
            stacklevel=find_stack_level(inspect.currentframe()),
        )
        return self.ffill(limit=limit)
