    def set_ordered(self, value, inplace=False):
        """
        Set the ordered attribute to the boolean value.

        Parameters
        ----------
        value : bool
           Set whether this categorical is ordered (True) or not (False).
        inplace : bool, default False
           Whether or not to set the ordered attribute in-place or return
           a copy of this categorical with ordered set to the value.
        """
        inplace = validate_bool_kwarg(inplace, "inplace")
        new_dtype = CategoricalDtype(self.categories, ordered=value)
        cat = self if inplace else self.copy()
        NDArrayBacked.__init__(cat, cat._ndarray, new_dtype)
        if not inplace:
            return cat
