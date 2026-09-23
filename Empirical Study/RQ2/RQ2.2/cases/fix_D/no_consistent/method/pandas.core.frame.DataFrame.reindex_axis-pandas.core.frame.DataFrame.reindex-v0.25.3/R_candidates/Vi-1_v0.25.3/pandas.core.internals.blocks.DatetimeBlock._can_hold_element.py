    def _can_hold_element(self, element):
        tipo = maybe_infer_dtype_type(element)
        if tipo is not None:
            if self.is_datetimetz:
                # require exact match, since non-nano does not exist
                return is_dtype_equal(tipo, self.dtype)

            # GH#27419 if we get a non-nano datetime64 object
            return is_datetime64_dtype(tipo)
        elif element is NaT:
            return True
        elif isinstance(element, datetime):
            if self.is_datetimetz:
                return tz_compare(element.tzinfo, self.dtype.tz)
            return element.tzinfo is None
        elif is_integer(element):
            return element == tslibs.iNaT

        return is_valid_nat_for_dtype(element, self.dtype)
