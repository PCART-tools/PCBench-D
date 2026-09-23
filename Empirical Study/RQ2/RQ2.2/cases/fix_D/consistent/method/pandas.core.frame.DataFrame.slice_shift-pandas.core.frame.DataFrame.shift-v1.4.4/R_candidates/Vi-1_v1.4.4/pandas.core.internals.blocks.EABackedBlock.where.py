    def where(self, other, cond) -> list[Block]:
        arr = self.values.T

        cond = extract_bool_array(cond)

        other = self._maybe_squeeze_arg(other)
        cond = self._maybe_squeeze_arg(cond)

        if other is lib.no_default:
            other = self.fill_value

        icond, noop = validate_putmask(arr, ~cond)
        if noop:
            # GH#44181, GH#45135
            # Avoid a) raising for Interval/PeriodDtype and b) unnecessary object upcast
            return self.copy()

        try:
            res_values = arr._where(cond, other).T
        except (ValueError, TypeError) as err:
            _catch_deprecated_value_error(err)

            if is_interval_dtype(self.dtype):
                # TestSetitemFloatIntervalWithIntIntervalValues
                blk = self.coerce_to_target_dtype(other)
                if blk.dtype == _dtype_obj:
                    # For now at least only support casting e.g.
                    #  Interval[int64]->Interval[float64]
                    raise
                return blk.where(other, cond)

            elif isinstance(self, NDArrayBackedExtensionBlock):
                # NB: not (yet) the same as
                #  isinstance(values, NDArrayBackedExtensionArray)
                if isinstance(self.dtype, PeriodDtype):
                    # TODO: don't special-case
                    raise
                blk = self.coerce_to_target_dtype(other)
                nbs = blk.where(other, cond)
                return self._maybe_downcast(nbs, "infer")

            else:
                raise

        nb = self.make_block_same_class(res_values)
        return [nb]
