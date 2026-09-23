    @final
    def _maybe_check_unique(self):
        """
        Check that an Index has no duplicates.

        This is typically only called via
        `NDFrame.flags.allows_duplicate_labels.setter` when it's set to
        True (duplicates aren't allowed).

        Raises
        ------
        DuplicateLabelError
            When the index is not unique.
        """
        if not self.is_unique:
            msg = """Index has duplicates."""
            duplicates = self._format_duplicate_message()
            msg += f"\n{duplicates}"

            raise DuplicateLabelError(msg)
