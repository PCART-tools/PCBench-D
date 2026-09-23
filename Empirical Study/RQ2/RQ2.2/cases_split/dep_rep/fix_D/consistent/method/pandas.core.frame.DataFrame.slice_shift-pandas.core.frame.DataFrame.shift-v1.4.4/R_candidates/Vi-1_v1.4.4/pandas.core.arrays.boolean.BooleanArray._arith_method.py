    def _arith_method(self, other, op):
        mask = None
        op_name = op.__name__

        if isinstance(other, BooleanArray):
            other, mask = other._data, other._mask

        elif is_list_like(other):
            other = np.asarray(other)
            if other.ndim > 1:
                raise NotImplementedError("can only perform ops with 1-d structures")
            if len(self) != len(other):
                raise ValueError("Lengths must match")

        # nans propagate
        if mask is None:
            mask = self._mask
            if other is libmissing.NA:
                mask |= True
        else:
            mask = self._mask | mask

        if other is libmissing.NA:
            # if other is NA, the result will be all NA and we can't run the
            # actual op, so we need to choose the resulting dtype manually
            if op_name in {"floordiv", "rfloordiv", "mod", "rmod", "pow", "rpow"}:
                dtype = "int8"
            elif op_name in {"truediv", "rtruediv"}:
                dtype = "float64"
            else:
                dtype = "bool"
            result = np.zeros(len(self._data), dtype=dtype)
        else:
            if op_name in {"pow", "rpow"} and isinstance(other, np.bool_):
                # Avoid DeprecationWarning: In future, it will be an error
                #  for 'np.bool_' scalars to be interpreted as an index
                other = bool(other)

            with np.errstate(all="ignore"):
                result = op(self._data, other)

        # divmod returns a tuple
        if op_name == "divmod":
            div, mod = result
            return (
                self._maybe_mask_result(div, mask, other, "floordiv"),
                self._maybe_mask_result(mod, mask, other, "mod"),
            )

        return self._maybe_mask_result(result, mask, other, op_name)
