    def equals(self, other):
        """
        Returns True if categorical arrays are equal.

        Parameters
        ----------
        other : `Categorical`

        Returns
        -------
        bool
        """
        if self.is_dtype_equal(other):
            if self.categories.equals(other.categories):
                # fastpath to avoid re-coding
                other_codes = other._codes
            else:
                other_codes = _recode_for_categories(
                    other.codes, other.categories, self.categories
                )
            return np.array_equal(self._codes, other_codes)
        return False
