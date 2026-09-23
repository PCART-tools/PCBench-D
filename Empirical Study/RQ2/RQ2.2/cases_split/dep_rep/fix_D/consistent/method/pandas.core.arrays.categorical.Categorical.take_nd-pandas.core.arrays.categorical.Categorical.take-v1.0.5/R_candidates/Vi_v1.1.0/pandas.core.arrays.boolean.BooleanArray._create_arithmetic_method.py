    @classmethod
    def _create_arithmetic_method(cls, op):
        op_name = op.__name__

        def boolean_arithmetic_method(self, other):

            if isinstance(other, (ABCDataFrame, ABCSeries, ABCIndexClass)):
                # Rely on pandas to unbox and dispatch to us.
                return NotImplemented

            other = lib.item_from_zerodim(other)
            mask = None

            if isinstance(other, BooleanArray):
                other, mask = other._data, other._mask

            elif is_list_like(other):
                other = np.asarray(other)
                if other.ndim > 1:
                    raise NotImplementedError(
                        "can only perform ops with 1-d structures"
                    )
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
                else:
                    dtype = "bool"
                result = np.zeros(len(self._data), dtype=dtype)
            else:
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

        name = f"__{op_name}__"
        return set_function_name(boolean_arithmetic_method, name, cls)
