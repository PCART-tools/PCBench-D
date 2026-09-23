    @final
    @cache_readonly
    def is_categorical(self) -> bool:
        warnings.warn(
            "Block.is_categorical is deprecated and will be removed in a "
            "future version.  Use isinstance(block.values, Categorical) "
            "instead. See https://github.com/pandas-dev/pandas/issues/40226",
            DeprecationWarning,
            stacklevel=find_stack_level(),
        )
        return isinstance(self.values, Categorical)
