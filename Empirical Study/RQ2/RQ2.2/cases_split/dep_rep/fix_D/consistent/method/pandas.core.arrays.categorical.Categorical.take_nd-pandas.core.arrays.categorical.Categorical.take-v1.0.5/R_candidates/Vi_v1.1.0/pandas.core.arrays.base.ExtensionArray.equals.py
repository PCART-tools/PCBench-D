    def equals(self, other: "ExtensionArray") -> bool:
        """
        Return if another array is equivalent to this array.

        Equivalent means that both arrays have the same shape and dtype, and
        all values compare equal. Missing values in the same location are
        considered equal (in contrast with normal equality).

        Parameters
        ----------
        other : ExtensionArray
            Array to compare to this Array.

        Returns
        -------
        boolean
            Whether the arrays are equivalent.
        """
        if not type(self) == type(other):
            return False
        elif not self.dtype == other.dtype:
            return False
        elif not len(self) == len(other):
            return False
        else:
            equal_values = self == other
            if isinstance(equal_values, ExtensionArray):
                # boolean array with NA -> fill with False
                equal_values = equal_values.fillna(False)
            equal_na = self.isna() & other.isna()
            return bool((equal_values | equal_na).all())
