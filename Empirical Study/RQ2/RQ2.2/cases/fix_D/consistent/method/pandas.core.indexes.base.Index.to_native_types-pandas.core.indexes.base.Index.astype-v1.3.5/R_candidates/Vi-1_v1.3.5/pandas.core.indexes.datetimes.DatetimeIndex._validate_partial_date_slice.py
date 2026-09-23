    def _validate_partial_date_slice(self, reso: Resolution):
        assert isinstance(reso, Resolution), (type(reso), reso)
        if (
            self.is_monotonic
            and reso.attrname in ["day", "hour", "minute", "second"]
            and self._resolution_obj >= reso
        ):
            # These resolution/monotonicity validations came from GH3931,
            # GH3452 and GH2369.

            # See also GH14826
            raise KeyError

        if reso.attrname == "microsecond":
            # _partial_date_slice doesn't allow microsecond resolution, but
            # _parsed_string_to_bounds allows it.
            raise KeyError
