    def is_type_compatible(self, kind: str_t) -> bool:
        """
        Whether the index type is compatible with the provided type.
        """
        warnings.warn(
            "Index.is_type_compatible is deprecated and will be removed in a "
            "future version.",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return kind == self.inferred_type
