    @deprecate_renamed_function("total_days", version="0.19.13")
    def days(self) -> Expr:
        """
        Extract the total days from a Duration type.

        .. deprecated:: 0.19.13
            Use :meth:`total_days` instead.

        """
        return self.total_days()
