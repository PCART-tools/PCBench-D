    def is_dtype_equal(self, other):
        """
        Returns True if categoricals are the same dtype
          same categories, and same ordered

        Parameters
        ----------
        other : Categorical

        Returns
        -------
        are_equal : boolean
        """

        try:
            return (self.categories.equals(other.categories) and
                    self.ordered == other.ordered)
        except (AttributeError, TypeError):
            return False
