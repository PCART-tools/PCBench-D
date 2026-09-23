    @property
    @doc(DataFrame.dtypes.__doc__)
    def dtypes(self) -> Series:
        # GH#51045
        warnings.warn(
            f"{type(self).__name__}.dtypes is deprecated and will be removed in "
            "a future version. Check the dtypes on the base object instead",
            FutureWarning,
            stacklevel=find_stack_level(),
        )

        # error: Incompatible return value type (got "DataFrame", expected "Series")
        return self._python_apply_general(  # type: ignore[return-value]
            lambda df: df.dtypes, self._selected_obj
        )
