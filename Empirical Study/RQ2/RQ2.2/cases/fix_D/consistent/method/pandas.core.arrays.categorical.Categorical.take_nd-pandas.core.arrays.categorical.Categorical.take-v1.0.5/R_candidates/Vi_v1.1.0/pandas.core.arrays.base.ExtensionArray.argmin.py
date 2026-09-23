    def argmin(self):
        """
        Return the index of minimum value.

        In case of multiple occurrences of the minimum value, the index
        corresponding to the first occurrence is returned.

        Returns
        -------
        int

        See Also
        --------
        ExtensionArray.argmax
        """
        return nargminmax(self, "argmin")
