    def _construct_axes_from_arguments(self, args, kwargs, require_all=False):
        """Construct and returns axes if supplied in args/kwargs.

        If require_all, raise if all axis arguments are not supplied
        return a tuple of (axes, kwargs).
        """

        # construct the args
        args = list(args)
        for a in self._AXIS_ORDERS:

            # if we have an alias for this axis
            alias = self._AXIS_IALIASES.get(a)
            if alias is not None:
                if a in kwargs:
                    if alias in kwargs:
                        raise TypeError("arguments are mutually exclusive "
                                        "for [%s,%s]" % (a, alias))
                    continue
                if alias in kwargs:
                    kwargs[a] = kwargs.pop(alias)
                    continue

            # look for a argument by position
            if a not in kwargs:
                try:
                    kwargs[a] = args.pop(0)
                except IndexError:
                    if require_all:
                        raise TypeError("not enough/duplicate arguments "
                                        "specified!")

        axes = dict([(a, kwargs.pop(a, None)) for a in self._AXIS_ORDERS])
        return axes, kwargs
