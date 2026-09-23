    @deprecate_renamed_function("gather_every", version="0.19.14")
    def take_every(self, n: int, offset: int = 0) -> Self:
        """
        Take every nth row in the LazyFrame and return as a new LazyFrame.

        .. deprecated:: 0.19.0
            This method has been renamed to :meth:`gather_every`.

        Parameters
        ----------
        n
            Gather every *n*-th row.
        offset
            Starting index.
        """
        return self.gather_every(n, offset)
