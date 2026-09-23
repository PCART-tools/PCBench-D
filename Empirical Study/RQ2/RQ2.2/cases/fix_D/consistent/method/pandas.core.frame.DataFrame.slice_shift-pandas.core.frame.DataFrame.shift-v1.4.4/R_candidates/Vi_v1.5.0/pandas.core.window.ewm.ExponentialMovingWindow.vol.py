    def vol(self, bias: bool = False, *args, **kwargs):
        warnings.warn(
            (
                "vol is deprecated will be removed in a future version. "
                "Use std instead."
            ),
            FutureWarning,
            stacklevel=find_stack_level(inspect.currentframe()),
        )
        return self.std(bias, *args, **kwargs)
