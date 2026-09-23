    def _partial_date_slice(self, reso, parsed, use_lhs=True, use_rhs=True):
        is_monotonic = self.is_monotonic
        if (is_monotonic and reso in ['day', 'hour', 'minute', 'second'] and
                self._resolution >= Resolution.get_reso(reso)):
            # These resolution/monotonicity validations came from GH3931,
            # GH3452 and GH2369.

            # See also GH14826
            raise KeyError

        if reso == 'microsecond':
            # _partial_date_slice doesn't allow microsecond resolution, but
            # _parsed_string_to_bounds allows it.
            raise KeyError

        t1, t2 = self._parsed_string_to_bounds(reso, parsed)
        stamps = self.asi8

        if is_monotonic:

            # we are out of range
            if (len(stamps) and ((use_lhs and t1.value < stamps[0] and
                                  t2.value < stamps[0]) or
                                 ((use_rhs and t1.value > stamps[-1] and
                                   t2.value > stamps[-1])))):
                raise KeyError

            # a monotonic (sorted) series can be sliced
            left = stamps.searchsorted(
                t1.value, side='left') if use_lhs else None
            right = stamps.searchsorted(
                t2.value, side='right') if use_rhs else None

            return slice(left, right)

        lhs_mask = (stamps >= t1.value) if use_lhs else True
        rhs_mask = (stamps <= t2.value) if use_rhs else True

        # try to find a the dates
        return (lhs_mask & rhs_mask).nonzero()[0]
