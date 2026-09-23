    @deprecate_kwarg(old_arg_name="labels", new_arg_name="codes")
    def __new__(
        cls,
        levels=None,
        codes=None,
        sortorder=None,
        names=None,
        dtype=None,
        copy=False,
        name=None,
        verify_integrity=True,
        _set_identity=True,
    ):

        # compat with Index
        if name is not None:
            names = name
        if levels is None or codes is None:
            raise TypeError("Must pass both levels and codes")
        if len(levels) != len(codes):
            raise ValueError("Length of levels and codes must be the same.")
        if len(levels) == 0:
            raise ValueError("Must pass non-zero number of levels/codes")

        result = object.__new__(MultiIndex)

        # we've already validated levels and codes, so shortcut here
        result._set_levels(levels, copy=copy, validate=False)
        result._set_codes(codes, copy=copy, validate=False)

        if names is not None:
            # handles name validation
            result._set_names(names)

        if sortorder is not None:
            result.sortorder = int(sortorder)
        else:
            result.sortorder = sortorder

        if verify_integrity:
            new_codes = result._verify_integrity()
            result._codes = new_codes

        if _set_identity:
            result._reset_identity()

        return result
