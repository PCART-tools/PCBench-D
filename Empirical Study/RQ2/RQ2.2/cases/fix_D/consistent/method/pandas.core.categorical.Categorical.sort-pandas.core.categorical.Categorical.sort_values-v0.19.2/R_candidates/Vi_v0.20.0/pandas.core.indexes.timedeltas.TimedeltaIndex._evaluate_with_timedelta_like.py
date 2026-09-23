    def _evaluate_with_timedelta_like(self, other, op, opstr):

        # allow division by a timedelta
        if opstr in ['__div__', '__truediv__', '__floordiv__']:
            if _is_convertible_to_td(other):
                other = Timedelta(other)
                if isnull(other):
                    raise NotImplementedError(
                        "division by pd.NaT not implemented")

                i8 = self.asi8
                if opstr in ['__floordiv__']:
                    result = i8 // other.value
                else:
                    result = op(i8, float(other.value))
                result = self._maybe_mask_results(result, convert='float64')
                return Index(result, name=self.name, copy=False)

        return NotImplemented
