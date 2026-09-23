    @final
    def ravel(self, order: str_t = "C") -> Index:
        """
        Return a view on self.

        Returns
        -------
        Index

        See Also
        --------
        numpy.ndarray.ravel : Return a flattened array.
        """
        return self[:]
