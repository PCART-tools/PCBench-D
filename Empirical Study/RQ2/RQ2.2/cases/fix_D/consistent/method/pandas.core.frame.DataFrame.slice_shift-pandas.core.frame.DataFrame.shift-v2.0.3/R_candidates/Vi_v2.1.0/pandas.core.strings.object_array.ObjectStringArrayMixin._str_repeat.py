    def _str_repeat(self, repeats: int | Sequence[int]):
        if lib.is_integer(repeats):
            rint = cast(int, repeats)

            def scalar_rep(x):
                try:
                    return bytes.__mul__(x, rint)
                except TypeError:
                    return str.__mul__(x, rint)

            return self._str_map(scalar_rep, dtype=str)
        else:
            from pandas.core.arrays.string_ import BaseStringArray

            def rep(x, r):
                if x is libmissing.NA:
                    return x
                try:
                    return bytes.__mul__(x, r)
                except TypeError:
                    return str.__mul__(x, r)

            result = libops.vec_binop(
                np.asarray(self),
                np.asarray(repeats, dtype=object),
                rep,
            )
            if isinstance(self, BaseStringArray):
                # Not going through map, so we have to do this here.
                result = type(self)._from_sequence(result)
            return result
