    @deprecate_renamed_function("total_minutes", version="0.19.13")
    def minutes(self) -> Series:
        """
        Extract the total minutes from a Duration type.

        .. deprecated:: 0.19.13
            Use :meth:`total_minutes` instead.

        """
        return self.total_minutes()
