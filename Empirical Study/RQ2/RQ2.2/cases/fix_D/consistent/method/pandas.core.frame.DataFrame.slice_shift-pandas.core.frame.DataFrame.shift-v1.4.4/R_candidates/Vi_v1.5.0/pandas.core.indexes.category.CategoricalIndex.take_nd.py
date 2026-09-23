    def take_nd(self, *args, **kwargs) -> CategoricalIndex:
        """Alias for `take`"""
        warnings.warn(
            "CategoricalIndex.take_nd is deprecated, use CategoricalIndex.take "
            "instead.",
            FutureWarning,
            stacklevel=find_stack_level(inspect.currentframe()),
        )
        return self.take(*args, **kwargs)
