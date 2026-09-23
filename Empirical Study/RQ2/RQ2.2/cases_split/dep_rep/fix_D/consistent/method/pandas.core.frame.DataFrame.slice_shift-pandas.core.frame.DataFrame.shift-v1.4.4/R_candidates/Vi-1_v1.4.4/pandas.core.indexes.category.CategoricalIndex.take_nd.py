    def take_nd(self, *args, **kwargs):
        """Alias for `take`"""
        warnings.warn(
            "CategoricalIndex.take_nd is deprecated, use CategoricalIndex.take "
            "instead.",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return self.take(*args, **kwargs)
