    def _maybe_coerce_values(self, values):
        """Unbox to an extension array.

        This will unbox an ExtensionArray stored in an Index or Series.
        ExtensionArrays pass through. No dtype coercion is done.

        Parameters
        ----------
        values : Index, Series, ExtensionArray

        Returns
        -------
        ExtensionArray
        """
        if isinstance(values, (ABCIndexClass, ABCSeries)):
            values = values._values
        return values
