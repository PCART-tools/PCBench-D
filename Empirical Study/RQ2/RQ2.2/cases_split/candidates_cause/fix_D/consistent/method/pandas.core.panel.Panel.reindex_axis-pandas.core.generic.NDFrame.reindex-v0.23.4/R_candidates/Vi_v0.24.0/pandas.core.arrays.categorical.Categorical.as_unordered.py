    def as_unordered(self, inplace=False):
        """
        Set the Categorical to be unordered.

        Parameters
        ----------
        inplace : boolean (default: False)
           Whether or not to set the ordered attribute inplace or return a copy
           of this categorical with ordered set to False
        """
        inplace = validate_bool_kwarg(inplace, 'inplace')
        return self.set_ordered(False, inplace=inplace)
