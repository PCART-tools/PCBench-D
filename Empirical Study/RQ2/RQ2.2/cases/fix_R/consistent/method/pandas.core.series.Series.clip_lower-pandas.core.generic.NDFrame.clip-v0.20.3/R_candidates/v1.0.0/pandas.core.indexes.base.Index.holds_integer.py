    def holds_integer(self):
        """
        Whether the type is an integer type.
        """
        return self.inferred_type in ["integer", "mixed-integer"]
