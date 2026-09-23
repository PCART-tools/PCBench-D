    def _maybe_warn_numeric_only_depr(
        self, how: str, result: DataFrame | Series, numeric_only: bool | lib.NoDefault
    ) -> None:
        """Emit warning on numeric_only behavior deprecation when appropriate.

        Parameters
        ----------
        how : str
            Groupby kernel name.
        result :
            Result of the groupby operation.
        numeric_only : bool or lib.no_default
            Argument as passed by user.
        """
        if (
            self._obj_with_exclusions.ndim != 1
            and result.ndim > 1
            and len(result.columns) < len(self._obj_with_exclusions.columns)
        ):
            warn_dropping_nuisance_columns_deprecated(type(self), how, numeric_only)
