    @final
    def _holds_integer(self) -> bool:
        """
        Whether the type is an integer type.
        """
        return self.inferred_type in ["integer", "mixed-integer"]
