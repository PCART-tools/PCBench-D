    def _arith_method(self, other, op):
        op_name = op.__name__
        omask = None

        if (
            not hasattr(other, "dtype")
            and is_list_like(other)
            and len(other) == len(self)
        ):
            # Try inferring masked dtype instead of casting to object
            inferred_dtype = lib.infer_dtype(other, skipna=True)
            if inferred_dtype == "integer":
                from pandas.core.arrays import IntegerArray

                other = IntegerArray._from_sequence(other)
            elif inferred_dtype in ["floating", "mixed-integer-float"]:
                from pandas.core.arrays import FloatingArray

                other = FloatingArray._from_sequence(other)

            elif inferred_dtype in ["boolean"]:
                from pandas.core.arrays import BooleanArray

                other = BooleanArray._from_sequence(other)

        if isinstance(other, BaseMaskedArray):
            other, omask = other._data, other._mask

        elif is_list_like(other):
            if not isinstance(other, ExtensionArray):
                other = np.asarray(other)
            if other.ndim > 1:
                raise NotImplementedError("can only perform ops with 1-d structures")

        # We wrap the non-masked arithmetic logic used for numpy dtypes
        #  in Series/Index arithmetic ops.
        other = ops.maybe_prepare_scalar_for_op(other, (len(self),))
        pd_op = ops.get_array_op(op)
        other = ensure_wrapped_if_datetimelike(other)

        if op_name in {"pow", "rpow"} and isinstance(other, np.bool_):
            # Avoid DeprecationWarning: In future, it will be an error
            #  for 'np.bool_' scalars to be interpreted as an index
            #  e.g. test_array_scalar_like_equivalence
            other = bool(other)

        mask = self._propagate_mask(omask, other)

        if other is libmissing.NA:
            result = np.ones_like(self._data)
            if self.dtype.kind == "b":
                if op_name in {
                    "floordiv",
                    "rfloordiv",
                    "pow",
                    "rpow",
                    "truediv",
                    "rtruediv",
                }:
                    # GH#41165 Try to match non-masked Series behavior
                    #  This is still imperfect GH#46043
                    raise NotImplementedError(
                        f"operator '{op_name}' not implemented for bool dtypes"
                    )
                if op_name in {"mod", "rmod"}:
                    dtype = "int8"
                else:
                    dtype = "bool"
                result = result.astype(dtype)
            elif "truediv" in op_name and self.dtype.kind != "f":
                # The actual data here doesn't matter since the mask
                #  will be all-True, but since this is division, we want
                #  to end up with floating dtype.
                result = result.astype(np.float64)
        else:
            # Make sure we do this before the "pow" mask checks
            #  to get an expected exception message on shape mismatch.
            if self.dtype.kind in ["i", "u"] and op_name in ["floordiv", "mod"]:
                # TODO(GH#30188) ATM we don't match the behavior of non-masked
                #  types with respect to floordiv-by-zero
                pd_op = op

            with np.errstate(all="ignore"):
                result = pd_op(self._data, other)

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

        return self._maybe_mask_result(result, mask)
