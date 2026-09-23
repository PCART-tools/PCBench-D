    def root_names(self) -> list[str]:
        """
        Get a list with the root column name.

        Examples
        --------
        >>> e = pl.col("foo") * pl.col("bar")
        >>> e.meta.root_names()
        ['foo', 'bar']
        >>> e_filter = pl.col("foo").filter(pl.col("bar") == 13)
        >>> e_filter.meta.root_names()
        ['foo', 'bar']
        >>> e_sum_over = pl.sum("foo").over("groups")
        >>> e_sum_over.meta.root_names()
        ['foo', 'groups']
        >>> e_sum_slice = pl.sum("foo").slice(pl.len() - 10, pl.col("bar"))
        >>> e_sum_slice.meta.root_names()
        ['foo', 'bar']
        """
        return self._pyexpr.meta_root_names()
