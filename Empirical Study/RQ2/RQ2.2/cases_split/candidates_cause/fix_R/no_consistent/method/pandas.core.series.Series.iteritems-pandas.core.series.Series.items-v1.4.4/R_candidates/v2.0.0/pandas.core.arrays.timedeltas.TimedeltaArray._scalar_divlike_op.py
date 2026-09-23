    def _scalar_divlike_op(self, other, op):
        """
        Shared logic for __truediv__, __rtruediv__, __floordiv__, __rfloordiv__
        with scalar 'other'.
        """
        if isinstance(other, self._recognized_scalars):
            other = Timedelta(other)
            # mypy assumes that __new__ returns an instance of the class
            # github.com/python/mypy/issues/1020
            if cast("Timedelta | NaTType", other) is NaT:
                # specifically timedelta64-NaT
                result = np.empty(self.shape, dtype=np.float64)
                result.fill(np.nan)
                return result

            # otherwise, dispatch to Timedelta implementation
            return op(self._ndarray, other)

        else:
            # caller is responsible for checking lib.is_scalar(other)
            # assume other is numeric, otherwise numpy will raise

            if op in [roperator.rtruediv, roperator.rfloordiv]:
                raise TypeError(
                    f"Cannot divide {type(other).__name__} by {type(self).__name__}"
                )

            result = op(self._ndarray, other)
            freq = None

            if self.freq is not None:
                # Note: freq gets division, not floor-division, even if op
                #  is floordiv.
                freq = self.freq / other

                # TODO: 2022-12-24 test_ufunc_coercions, test_tdi_ops_attributes
                #  get here for truediv, no tests for floordiv

                if op is operator.floordiv:
                    if freq.nanos == 0 and self.freq.nanos != 0:
                        # e.g. if self.freq is Nano(1) then dividing by 2
                        #  rounds down to zero
                        # TODO: 2022-12-24 should implement the same check
                        #  for truediv case
                        freq = None

            return type(self)._simple_new(result, dtype=result.dtype, freq=freq)
