    @classmethod
    def _create_arithmetic_method(cls, op):
        op_name = op.__name__

        @unpack_zerodim_and_defer(op.__name__)
        def integer_arithmetic_method(self, other):

            omask = None

            if getattr(other, "ndim", 0) > 1:
                raise NotImplementedError("can only perform ops with 1-d structures")

            if isinstance(other, IntegerArray):
                other, omask = other._data, other._mask

            elif is_list_like(other):
                other = np.asarray(other)
                if other.ndim > 1:
                    raise NotImplementedError(
                        "can only perform ops with 1-d structures"
                    )
                if len(self) != len(other):
                    raise ValueError("Lengths must match")
                if not (is_float_dtype(other) or is_integer_dtype(other)):
                    raise TypeError("can only perform ops with numeric values")

            else:
                if not (is_float(other) or is_integer(other) or other is libmissing.NA):
                    raise TypeError("can only perform ops with numeric values")

            if omask is None:
                mask = self._mask.copy()
                if other is libmissing.NA:
                    mask |= True
            else:
                mask = self._mask | omask

            if op_name == "pow":
                # 1 ** x is 1.
                mask = np.where((self._data == 1) & ~self._mask, False, mask)
                # x ** 0 is 1.
                if omask is not None:
                    mask = np.where((other == 0) & ~omask, False, mask)
                elif other is not libmissing.NA:
                    mask = np.where(other == 0, False, mask)

            elif op_name == "rpow":
                # 1 ** x is 1.
                if omask is not None:
                    mask = np.where((other == 1) & ~omask, False, mask)
                elif other is not libmissing.NA:
                    mask = np.where(other == 1, False, mask)
                # x ** 0 is 1.
                mask = np.where((self._data == 0) & ~self._mask, False, mask)

            if other is libmissing.NA:
                result = np.ones_like(self._data)
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

        name = f"__{op.__name__}__"
        return set_function_name(integer_arithmetic_method, name, cls)
