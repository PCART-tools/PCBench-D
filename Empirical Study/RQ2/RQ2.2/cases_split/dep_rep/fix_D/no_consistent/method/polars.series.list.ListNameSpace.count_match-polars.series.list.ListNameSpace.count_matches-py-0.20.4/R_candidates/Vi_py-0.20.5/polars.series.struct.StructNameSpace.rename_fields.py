    def rename_fields(self, names: Sequence[str]) -> Series:
        """
        Rename the fields of the struct.

        Parameters
        ----------
        names
            New names in the order of the struct's fields
        """
