    def _str_repeat(self, repeats):
        if is_scalar(repeats):

            def scalar_rep(x):
                try:
                    return bytes.__mul__(x, repeats)
                except TypeError:
                    return str.__mul__(x, repeats)

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

            repeats = np.asarray(repeats, dtype=object)
            result = libops.vec_binop(np.asarray(self), repeats, rep)
            if isinstance(self, BaseStringArray):
                # Not going through map, so we have to do this here.
                result = type(self)._from_sequence(result)
            return result
