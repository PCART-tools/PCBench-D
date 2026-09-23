    def is_type_compatible(self, kind: str_t) -> bool:
        """
        Whether the index type is compatible with the provided type.
        """
        return kind == self.inferred_type
