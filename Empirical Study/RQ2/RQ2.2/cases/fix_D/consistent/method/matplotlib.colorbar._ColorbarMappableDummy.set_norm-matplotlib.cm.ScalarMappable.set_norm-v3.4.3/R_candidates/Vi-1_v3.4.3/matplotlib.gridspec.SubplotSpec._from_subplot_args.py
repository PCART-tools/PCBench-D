    @staticmethod
    def _from_subplot_args(figure, args):
        """
        Construct a `.SubplotSpec` from a parent `.Figure` and either

        - a `.SubplotSpec` -- returned as is;
        - one or three numbers -- a MATLAB-style subplot specifier.
        """
        message = ("Passing non-integers as three-element position "
                   "specification is deprecated since %(since)s and will be "
                   "removed %(removal)s.")
        if len(args) == 1:
            arg, = args
            if isinstance(arg, SubplotSpec):
                return arg
            else:
                if not isinstance(arg, Integral):
                    _api.warn_deprecated("3.3", message=message)
                    arg = str(arg)
                try:
                    rows, cols, num = map(int, str(arg))
                except ValueError:
                    raise ValueError(
                        f"Single argument to subplot must be a three-digit "
                        f"integer, not {arg}") from None
                i = j = num
        elif len(args) == 3:
            rows, cols, num = args
            if not (isinstance(rows, Integral) and isinstance(cols, Integral)):
                _api.warn_deprecated("3.3", message=message)
                rows, cols = map(int, [rows, cols])
            gs = GridSpec(rows, cols, figure=figure)
            if isinstance(num, tuple) and len(num) == 2:
                if not all(isinstance(n, Integral) for n in num):
                    _api.warn_deprecated("3.3", message=message)
                    i, j = map(int, num)
                else:
                    i, j = num
            else:
                if not isinstance(num, Integral):
                    _api.warn_deprecated("3.3", message=message)
                    num = int(num)
                if num < 1 or num > rows*cols:
                    raise ValueError(
                        f"num must be 1 <= num <= {rows*cols}, not {num}")
                i = j = num
        else:
            raise TypeError(f"subplot() takes 1 or 3 positional arguments but "
                            f"{len(args)} were given")

        gs = GridSpec._check_gridspec_exists(figure, rows, cols)
        if gs is None:
            gs = GridSpec(rows, cols, figure=figure)
        return gs[i-1:j]
