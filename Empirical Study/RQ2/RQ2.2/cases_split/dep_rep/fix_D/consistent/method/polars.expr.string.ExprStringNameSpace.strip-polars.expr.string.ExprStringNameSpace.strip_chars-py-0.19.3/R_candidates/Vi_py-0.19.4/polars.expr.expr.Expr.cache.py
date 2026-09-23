    @deprecate_function(
        "This method now does nothing. It has been superseded by the"
        " `comm_subexpr_elim` setting on `LazyFrame.collect`, which automatically"
        " caches expressions that are equal.",
        version="0.18.9",
    )
    def cache(self) -> Self:
        """
        Cache this expression so that it only is executed once per context.

        .. deprecated:: 0.18.9
            This method now does nothing. It has been superseded by the
            `comm_subexpr_elim` setting on `LazyFrame.collect`, which automatically
            caches expressions that are equal.

        """
        return self
