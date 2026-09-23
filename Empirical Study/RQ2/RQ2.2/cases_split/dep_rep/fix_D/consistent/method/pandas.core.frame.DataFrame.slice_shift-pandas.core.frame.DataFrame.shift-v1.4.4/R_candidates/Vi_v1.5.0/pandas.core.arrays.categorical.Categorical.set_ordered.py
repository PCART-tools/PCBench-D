    @deprecate_nonkeyword_arguments(version=None, allowed_args=["self", "value"])
    def set_ordered(
        self, value, inplace: bool | NoDefault = no_default
    ) -> Categorical | None:
        """
        Set the ordered attribute to the boolean value.

        Parameters
        ----------
        value : bool
           Set whether this categorical is ordered (True) or not (False).
        inplace : bool, default False
           Whether or not to set the ordered attribute in-place or return
           a copy of this categorical with ordered set to the value.

           .. deprecated:: 1.5.0

        """
        if inplace is not no_default:
            warn(
                "The `inplace` parameter in pandas.Categorical."
                "set_ordered is deprecated and will be removed in "
                "a future version. setting ordered-ness on categories will always "
                "return a new Categorical object.",
                FutureWarning,
                stacklevel=find_stack_level(inspect.currentframe()),
            )
        else:
            inplace = False

        inplace = validate_bool_kwarg(inplace, "inplace")
        new_dtype = CategoricalDtype(self.categories, ordered=value)
        cat = self if inplace else self.copy()
        NDArrayBacked.__init__(cat, cat._ndarray, new_dtype)
        if not inplace:
            return cat
        return None
