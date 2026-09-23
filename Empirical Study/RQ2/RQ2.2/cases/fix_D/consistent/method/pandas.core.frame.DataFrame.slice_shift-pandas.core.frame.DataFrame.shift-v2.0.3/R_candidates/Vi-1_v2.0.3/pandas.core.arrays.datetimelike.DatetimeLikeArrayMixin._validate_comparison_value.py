    def _validate_comparison_value(self, other):
        if isinstance(other, str):
            try:
                # GH#18435 strings get a pass from tzawareness compat
                other = self._scalar_from_string(other)
            except (ValueError, IncompatibleFrequency):
                # failed to parse as Timestamp/Timedelta/Period
                raise InvalidComparison(other)

        if isinstance(other, self._recognized_scalars) or other is NaT:
            other = self._scalar_type(other)
            try:
                self._check_compatible_with(other)
            except (TypeError, IncompatibleFrequency) as err:
                # e.g. tzawareness mismatch
                raise InvalidComparison(other) from err

        elif not is_list_like(other):
            raise InvalidComparison(other)

        elif len(other) != len(self):
            raise ValueError("Lengths must match")

        else:
            try:
                other = self._validate_listlike(other, allow_object=True)
                self._check_compatible_with(other)
            except (TypeError, IncompatibleFrequency) as err:
                if is_object_dtype(getattr(other, "dtype", None)):
                    # We will have to operate element-wise
                    pass
                else:
                    raise InvalidComparison(other) from err

        return other
