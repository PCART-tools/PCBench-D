    @deprecate_renamed_function("total_nanoseconds", version="0.19.13")
    def nanoseconds(self) -> Expr:
        """
        Extract the total nanoseconds from a Duration type.

        .. deprecated:: 0.19.13
            Use :meth:`total_nanoseconds` instead.
        """
        return self.total_nanoseconds()
