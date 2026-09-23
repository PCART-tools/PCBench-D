    def _expanddim_from_mgr(self, mgr, axes) -> DataFrame:
        # https://github.com/pandas-dev/pandas/pull/52132#issuecomment-1481491828
        #  This is a short-term implementation that will be replaced
        #  with self._constructor_expanddim._constructor_from_mgr(...)
        #  once downstream packages (geopandas) have had a chance to implement
        #  their own overrides.
        # error: "Callable[..., DataFrame]" has no attribute "_from_mgr"  [attr-defined]
        from pandas import DataFrame

        return DataFrame._from_mgr(mgr, axes=mgr.axes)
