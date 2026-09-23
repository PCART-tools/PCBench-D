    def putmask(self, mask, new) -> list[Block]:
        """
        See Block.putmask.__doc__
        """
        mask = extract_bool_array(mask)

        values = self.values

        mask = self._maybe_squeeze_arg(mask)

        try:
            # Caller is responsible for ensuring matching lengths
            values._putmask(mask, new)
        except (TypeError, ValueError) as err:
            _catch_deprecated_value_error(err)

            if is_interval_dtype(self.dtype):
                # Discussion about what we want to support in the general
                #  case GH#39584
                blk = self.coerce_to_target_dtype(new)
                if blk.dtype == _dtype_obj:
                    # For now at least, only support casting e.g.
                    #  Interval[int64]->Interval[float64],
                    raise
                return blk.putmask(mask, new)

            elif isinstance(self, NDArrayBackedExtensionBlock):
                # NB: not (yet) the same as
                #  isinstance(values, NDArrayBackedExtensionArray)
                if isinstance(self.dtype, PeriodDtype):
                    # TODO: don't special-case
                    raise
                blk = self.coerce_to_target_dtype(new)
                return blk.putmask(mask, new)

            else:
                raise

        return [self]
