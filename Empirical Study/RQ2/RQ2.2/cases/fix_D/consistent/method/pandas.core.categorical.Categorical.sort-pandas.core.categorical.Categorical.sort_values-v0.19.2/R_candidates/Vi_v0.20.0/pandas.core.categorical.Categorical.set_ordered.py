    def set_ordered(self, value, inplace=False):
        """
        Sets the ordered attribute to the boolean value

        Parameters
        ----------
        value : boolean to set whether this categorical is ordered (True) or
           not (False)
        inplace : boolean (default: False)
           Whether or not to set the ordered attribute inplace or return a copy
           of this categorical with ordered set to the value
        """
        inplace = validate_bool_kwarg(inplace, 'inplace')
        self._validate_ordered(value)
        cat = self if inplace else self.copy()
        cat._ordered = value
        if not inplace:
            return cat
