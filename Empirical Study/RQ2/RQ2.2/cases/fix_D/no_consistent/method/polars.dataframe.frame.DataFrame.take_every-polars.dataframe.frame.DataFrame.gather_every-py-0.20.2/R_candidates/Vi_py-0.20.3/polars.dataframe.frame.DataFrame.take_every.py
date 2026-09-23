    @deprecate_renamed_function("gather_every", version="0.19.12")
    def take_every(self, n: int, offset: int = 0) -> DataFrame:
        """
        Take every nth row in the DataFrame and return as a new DataFrame.

        .. deprecated:: 0.19.14
            This method has been renamed to :func:`gather_every`.

        Parameters
        ----------
        n
            Gather every *n*-th row.
        offset
            Starting index.
        """
        return self.gather_every(n, offset)
