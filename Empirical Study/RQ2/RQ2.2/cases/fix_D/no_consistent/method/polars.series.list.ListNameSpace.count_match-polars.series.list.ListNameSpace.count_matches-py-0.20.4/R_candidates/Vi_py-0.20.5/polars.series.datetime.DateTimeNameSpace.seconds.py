    @deprecate_renamed_function("total_seconds", version="0.19.13")
    def seconds(self) -> Series:
        """
        Extract the total seconds from a Duration type.

        .. deprecated:: 0.19.13
            Use :meth:`total_seconds` instead.
        """
        return self.total_seconds()
