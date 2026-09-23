    def _validate_converted_limits(self, limit, convert):
        """
        Raise ValueError if converted limits are non-finite.

        Note that this function also accepts None as a limit argument.

        Returns
        -------
        The limit value after call to convert(), or None if limit is None.

        """
        if limit is not None:
            converted_limit = convert(limit)
            if (isinstance(converted_limit, float) and
                    (not np.isreal(converted_limit) or
                        not np.isfinite(converted_limit))):
                raise ValueError("Axis limits cannot be NaN or Inf")
            return converted_limit
