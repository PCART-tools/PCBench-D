    def _validate_scalar(
        self, value, msg: Optional[str] = None, cast_str: bool = False
    ):
        """
        Validate that the input value can be cast to our scalar_type.

        Parameters
        ----------
        value : object
        msg : str, optional.
            Message to raise in TypeError on invalid input.
            If not provided, `value` is cast to a str and used
            as the message.
        cast_str : bool, default False
            Whether to try to parse string input to scalar_type.

        Returns
        -------
        self._scalar_type or NaT
        """
        if cast_str and isinstance(value, str):
            # NB: Careful about tzawareness
            try:
                value = self._scalar_from_string(value)
            except ValueError as err:
                raise TypeError(msg) from err

        elif is_valid_nat_for_dtype(value, self.dtype):
            # GH#18295
            value = NaT

        elif isinstance(value, self._recognized_scalars):
            value = self._scalar_type(value)  # type: ignore

        else:
            if msg is None:
                msg = str(value)
            raise TypeError(msg)

        return value
