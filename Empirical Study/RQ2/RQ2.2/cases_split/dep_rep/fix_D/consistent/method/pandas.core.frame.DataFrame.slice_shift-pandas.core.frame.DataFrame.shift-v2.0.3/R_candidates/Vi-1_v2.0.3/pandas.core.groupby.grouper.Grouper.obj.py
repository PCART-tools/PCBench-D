    @final
    @property
    def obj(self):
        warnings.warn(
            f"{type(self).__name__}.obj is deprecated and will be removed "
            "in a future version. Use GroupBy.indexer instead.",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return self._obj_deprecated
