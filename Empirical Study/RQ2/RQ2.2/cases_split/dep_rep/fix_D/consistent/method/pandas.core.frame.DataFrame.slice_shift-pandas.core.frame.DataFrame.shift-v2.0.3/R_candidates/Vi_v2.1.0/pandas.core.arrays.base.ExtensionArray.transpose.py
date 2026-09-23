    def transpose(self, *axes: int) -> ExtensionArray:
        """
        Return a transposed view on this array.

        Because ExtensionArrays are always 1D, this is a no-op.  It is included
        for compatibility with np.ndarray.
        """
        return self[:]
