    def dropna(self: ExtensionArrayT) -> ExtensionArrayT:
        """
        Return ExtensionArray without NA values.

        Returns
        -------
        pandas.api.extensions.ExtensionArray
        """
        # error: Unsupported operand type for ~ ("ExtensionArray")
        return self[~self.isna()]  # type: ignore[operator]
