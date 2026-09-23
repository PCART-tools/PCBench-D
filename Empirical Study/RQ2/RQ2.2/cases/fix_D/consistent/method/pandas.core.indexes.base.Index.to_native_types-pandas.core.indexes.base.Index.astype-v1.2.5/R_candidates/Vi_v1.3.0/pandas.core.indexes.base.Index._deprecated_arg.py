    @final
    def _deprecated_arg(self, value, name: str_t, methodname: str_t) -> None:
        """
        Issue a FutureWarning if the arg/kwarg is not no_default.
        """
        if value is not no_default:
            warnings.warn(
                f"'{name}' argument in {methodname} is deprecated "
                "and will be removed in a future version.  Do not pass it.",
                FutureWarning,
                stacklevel=3,
            )
