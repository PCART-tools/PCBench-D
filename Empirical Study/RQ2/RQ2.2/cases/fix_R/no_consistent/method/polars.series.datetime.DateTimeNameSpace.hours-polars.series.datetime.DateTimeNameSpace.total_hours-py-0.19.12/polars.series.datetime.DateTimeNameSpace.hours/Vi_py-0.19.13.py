    @deprecate_renamed_function("total_hours", version="0.19.13")
    def hours(self) -> Series:
        """
        Extract the total hours from a Duration type.

        .. deprecated:: 0.19.13
            Use :meth:`total_hours` instead.

        """
        return self.total_hours()
