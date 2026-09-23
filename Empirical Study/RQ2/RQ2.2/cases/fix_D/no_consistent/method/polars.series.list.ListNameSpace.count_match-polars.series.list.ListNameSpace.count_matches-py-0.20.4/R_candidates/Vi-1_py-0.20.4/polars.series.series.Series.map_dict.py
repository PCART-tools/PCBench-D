    @deprecate_function(
        "It has been renamed to `replace`."
        " The default behavior has changed to keep any values not present in the mapping unchanged."
        " Pass `default=None` to keep existing behavior.",
        version="0.19.16",
    )
    @deprecate_renamed_parameter("remapping", "mapping", version="0.19.16")
    def map_dict(
        self,
        mapping: dict[Any, Any],
        *,
        default: Any = None,
        return_dtype: PolarsDataType | None = None,
    ) -> Self:
        """
        Replace values in the Series using a remapping dictionary.

        .. deprecated:: 0.19.16
            This method has been renamed to :meth:`replace`. The default behavior
            has changed to keep any values not present in the mapping unchanged.
            Pass `default=None` to keep existing behavior.

        Parameters
        ----------
        mapping
            Dictionary containing the before/after values to map.
        default
            Value to use when the remapping dict does not contain the lookup value.
            Use `pl.first()`, to keep the original value.
        return_dtype
            Set return dtype to override automatic return dtype determination.
        """
        return self.replace(mapping, default=default, return_dtype=return_dtype)
