    def argmax(self):
        """
        Return the index of maximum value.

        In case of multiple occurrences of the maximum value, the index
        corresponding to the first occurrence is returned.

        Returns
        -------
        int

        See Also
        --------
        ExtensionArray.argmin
        """
        return nargminmax(self, "argmax")
