    def ravel(self, order: Literal["C", "F", "A", "K"] | None = "C") -> ExtensionArray:
        """
        Return a flattened view on this array.

        Parameters
        ----------
        order : {None, 'C', 'F', 'A', 'K'}, default 'C'

        Returns
        -------
        ExtensionArray

        Notes
        -----
        - Because ExtensionArrays are 1D-only, this is a no-op.
        - The "order" argument is ignored, is for compatibility with NumPy.

        Examples
        --------
        >>> pd.array([1, 2, 3]).ravel()
        <IntegerArray>
        [1, 2, 3]
        Length: 3, dtype: Int64
        """
        return self
