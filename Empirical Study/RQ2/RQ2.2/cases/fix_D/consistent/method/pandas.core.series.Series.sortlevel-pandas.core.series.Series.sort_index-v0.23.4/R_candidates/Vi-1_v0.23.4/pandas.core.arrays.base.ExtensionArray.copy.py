    def copy(self, deep=False):
        # type: (bool) -> ExtensionArray
        """Return a copy of the array.

        Parameters
        ----------
        deep : bool, default False
            Also copy the underlying data backing this array.

        Returns
        -------
        ExtensionArray
        """
        raise AbstractMethodError(self)
