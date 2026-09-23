    def _validation_error_message(self, value, allow_listlike: bool = False) -> str:
        """
        Construct an exception message on validation error.

        Some methods allow only scalar inputs, while others allow either scalar
        or listlike.

        Parameters
        ----------
        allow_listlike: bool, default False

        Returns
        -------
        str
        """
        if allow_listlike:
            msg = (
                f"value should be a '{self._scalar_type.__name__}', 'NaT', "
                f"or array of those. Got '{type(value).__name__}' instead."
            )
        else:
            msg = (
                f"value should be a '{self._scalar_type.__name__}' or 'NaT'. "
                f"Got '{type(value).__name__}' instead."
            )
        return msg
