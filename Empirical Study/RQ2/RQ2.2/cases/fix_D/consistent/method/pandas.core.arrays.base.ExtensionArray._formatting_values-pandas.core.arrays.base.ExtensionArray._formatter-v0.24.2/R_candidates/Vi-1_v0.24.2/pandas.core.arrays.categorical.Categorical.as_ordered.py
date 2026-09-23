    def as_ordered(self, inplace=False):
        """
        Set the Categorical to be ordered.

        Parameters
        ----------
        inplace : boolean (default: False)
           Whether or not to set the ordered attribute inplace or return a copy
           of this categorical with ordered set to True
        """
        inplace = validate_bool_kwarg(inplace, 'inplace')
        return self.set_ordered(True, inplace=inplace)
