    def _validate_scalar(
        self,
        value,
        *,
        allow_listlike: bool = False,
        setitem: bool = True,
        unbox: bool = True,
    ):
        """
        Validate that the input value can be cast to our scalar_type.

        Parameters
        ----------
        value : object
        allow_listlike: bool, default False
            When raising an exception, whether the message should say
            listlike inputs are allowed.
        setitem : bool, default True
            Whether to check compatibility with setitem strictness.
        unbox : bool, default True
            Whether to unbox the result before returning.  Note: unbox=False
            skips the setitem compatibility check.

        Returns
        -------
        self._scalar_type or NaT
        """
        if isinstance(value, self._scalar_type):
            pass

        elif isinstance(value, str):
            # NB: Careful about tzawareness
            try:
                value = self._scalar_from_string(value)
            except ValueError as err:
                msg = self._validation_error_message(value, allow_listlike)
                raise TypeError(msg) from err

        elif is_valid_na_for_dtype(value, self.dtype):
            # GH#18295
            value = NaT

        elif isna(value):
            # if we are dt64tz and value is dt64("NaT"), dont cast to NaT,
            #  or else we'll fail to raise in _unbox_scalar
            msg = self._validation_error_message(value, allow_listlike)
            raise TypeError(msg)

        elif isinstance(value, self._recognized_scalars):
            value = self._scalar_type(value)

        else:
            msg = self._validation_error_message(value, allow_listlike)
            raise TypeError(msg)

        if not unbox:
            # NB: In general NDArrayBackedExtensionArray will unbox here;
            #  this option exists to prevent a performance hit in
            #  TimedeltaIndex.get_loc
            return value
        return self._unbox_scalar(value, setitem=setitem)
