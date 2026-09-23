    @deprecate_renamed_function("total_milliseconds", version="0.19.13")
    def milliseconds(self) -> Expr:
        """
        Extract the total milliseconds from a Duration type.

        .. deprecated:: 0.19.13
            Use :meth:`total_milliseconds` instead.
        """
        return self.total_milliseconds()
