    @final
    @classmethod
    def _construct_axes_from_arguments(
        cls, args, kwargs, require_all: bool_t = False, sentinel=None
    ):
        """
        Construct and returns axes if supplied in args/kwargs.

        If require_all, raise if all axis arguments are not supplied
        return a tuple of (axes, kwargs).

        sentinel specifies the default parameter when an axis is not
        supplied; useful to distinguish when a user explicitly passes None
        in scenarios where None has special meaning.
        """
        # construct the args
        args = list(args)
        for a in cls._AXIS_ORDERS:

            # look for a argument by position
            if a not in kwargs:
                try:
                    kwargs[a] = args.pop(0)
                except IndexError as err:
                    if require_all:
                        raise TypeError(
                            "not enough/duplicate arguments specified!"
                        ) from err

        axes = {a: kwargs.pop(a, sentinel) for a in cls._AXIS_ORDERS}
        return axes, kwargs
