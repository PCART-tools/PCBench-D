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
                    cbook.warn_deprecated("3.3", message=message)
                    arg = str(arg)
                try:
                    rows, cols, num = map(int, str(arg))
                except ValueError:
                    raise ValueError(
                        f"Single argument to subplot must be a three-digit "
                        f"integer, not {arg}") from None
                # num - 1 for converting from MATLAB to python indexing
                return GridSpec(rows, cols, figure=figure)[num - 1]
        elif len(args) == 3:
            rows, cols, num = args
            if not (isinstance(rows, Integral) and isinstance(cols, Integral)):
                cbook.warn_deprecated("3.3", message=message)
                rows, cols = map(int, [rows, cols])
            gs = GridSpec(rows, cols, figure=figure)
            if isinstance(num, tuple) and len(num) == 2:
                if not all(isinstance(n, Integral) for n in num):
                    cbook.warn_deprecated("3.3", message=message)
                    i, j = map(int, num)
                else:
                    i, j = num
                return gs[i-1:j]
            else:
                if not isinstance(num, Integral):
                    cbook.warn_deprecated("3.3", message=message)
                    num = int(num)
                if num < 1 or num > rows*cols:
                    raise ValueError(
                        f"num must be 1 <= num <= {rows*cols}, not {num}")
                return gs[num - 1]   # -1 due to MATLAB indexing.
        else:
            raise TypeError(f"subplot() takes 1 or 3 positional arguments but "
                            f"{len(args)} were given")
