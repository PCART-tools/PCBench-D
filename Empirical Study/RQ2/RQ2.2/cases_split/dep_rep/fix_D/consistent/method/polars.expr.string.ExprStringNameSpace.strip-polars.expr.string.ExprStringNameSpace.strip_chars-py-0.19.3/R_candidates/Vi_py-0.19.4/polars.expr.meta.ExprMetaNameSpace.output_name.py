    def output_name(self, *, raise_if_undetermined: bool = True) -> str | None:
        """
        Get the column name that this expression would produce.

        It may not always be possible to determine the output name as that can depend
        on the schema of the context; in that case this will raise ``ComputeError`` if
        ``raise_if_undetermined`` is True (the default), or ``None`` otherwise.

        Examples
        --------
        >>> e = pl.col("foo") * pl.col("bar")
        >>> e.meta.output_name()
        'foo'
        >>> e_filter = pl.col("foo").filter(pl.col("bar") == 13)
        >>> e_filter.meta.output_name()
        'foo'
        >>> e_sum_over = pl.sum("foo").over("groups")
        >>> e_sum_over.meta.output_name()
        'foo'
        >>> e_sum_slice = pl.sum("foo").slice(pl.count() - 10, pl.col("bar"))
        >>> e_sum_slice.meta.output_name()
        'foo'
        >>> pl.count().meta.output_name()
        'count'

        """
        try:
            return self._pyexpr.meta_output_name()
        except ComputeError:
            if not raise_if_undetermined:
                return None
            raise
