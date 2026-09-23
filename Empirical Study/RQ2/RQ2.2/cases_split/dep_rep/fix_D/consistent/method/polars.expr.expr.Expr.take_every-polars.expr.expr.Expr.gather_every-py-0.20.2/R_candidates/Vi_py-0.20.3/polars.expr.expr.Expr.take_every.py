    @deprecate_renamed_function("gather_every", version="0.19.14")
    def take_every(self, n: int, offset: int = 0) -> Self:
        """
        Take every nth value in the Series and return as a new Series.

        .. deprecated:: 0.19.14
            This method has been renamed to :meth:`gather_every`.

        Parameters
        ----------
        n
            Gather every *n*-th row.
        offset
            Starting index.
        """
        return self.gather_every(n, offset)
