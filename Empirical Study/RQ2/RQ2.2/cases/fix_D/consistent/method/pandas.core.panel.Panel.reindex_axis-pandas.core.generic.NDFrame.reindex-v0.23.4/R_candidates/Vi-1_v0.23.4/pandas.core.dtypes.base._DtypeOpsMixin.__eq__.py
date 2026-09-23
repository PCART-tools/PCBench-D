    def __eq__(self, other):
        """Check whether 'other' is equal to self.

        By default, 'other' is considered equal if

        * it's a string matching 'self.name'.
        * it's an instance of this type.

        Parameters
        ----------
        other : Any

        Returns
        -------
        bool
        """
        if isinstance(other, compat.string_types):
            return other == self.name
        elif isinstance(other, type(self)):
            return True
        else:
            return False
