    @property
    def flags(self) -> dict[str, dict[str, bool]]:
        """
        Get flags that are set on the columns of this DataFrame.

        Returns
        -------
        dict
            Mapping from column names to column flags.
        """
        return {name: self[name].flags for name in self.columns}
