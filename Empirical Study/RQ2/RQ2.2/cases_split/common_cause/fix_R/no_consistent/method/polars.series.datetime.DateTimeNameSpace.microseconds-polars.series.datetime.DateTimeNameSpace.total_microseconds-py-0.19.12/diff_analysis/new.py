    @deprecate_renamed_function("total_microseconds", version="0.19.13")
    def microseconds(self) -> Series:
        """
        Extract the total microseconds from a Duration type.

        .. deprecated:: 0.19.13
            Use :meth:`total_microseconds` instead.

        """
        return self.total_microseconds()
