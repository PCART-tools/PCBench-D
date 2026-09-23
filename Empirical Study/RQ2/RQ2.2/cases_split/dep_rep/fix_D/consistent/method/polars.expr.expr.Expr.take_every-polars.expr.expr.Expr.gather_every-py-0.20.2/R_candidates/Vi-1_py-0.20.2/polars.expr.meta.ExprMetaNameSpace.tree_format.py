    @deprecate_nonkeyword_arguments(version="0.19.3")
    def tree_format(self, return_as_string: bool = False) -> str | None:  # noqa: FBT001
        """
        Format the expression as a tree.

        Parameters
        ----------
        return_as_string:
            If True, return as string rather than printing to stdout.

        Examples
        --------
        >>> e = (pl.col("foo") * pl.col("bar")).sum().over(pl.col("ham")) / 2
        >>> e.meta.tree_format(return_as_string=True)  # doctest: +SKIP

        """
        s = self._pyexpr.meta_tree_format()
        if return_as_string:
            return s
        else:
            print(s)
            return None
