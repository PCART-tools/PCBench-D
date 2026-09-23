    @final
    @property
    def indexer(self):
        warnings.warn(
            f"{type(self).__name__}.indexer is deprecated and will be removed "
            "in a future version. Use Resampler.indexer instead.",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return self._indexer_deprecated
