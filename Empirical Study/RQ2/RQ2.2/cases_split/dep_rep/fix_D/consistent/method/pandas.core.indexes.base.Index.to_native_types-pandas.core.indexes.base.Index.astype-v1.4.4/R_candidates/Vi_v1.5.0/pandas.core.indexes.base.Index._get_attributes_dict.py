    @final
    def _get_attributes_dict(self) -> dict[str_t, Any]:
        """
        Return an attributes dict for my class.

        Temporarily added back for compatibility issue in dask, see
        https://github.com/pandas-dev/pandas/pull/43895
        """
        warnings.warn(
            "The Index._get_attributes_dict method is deprecated, and will be "
            "removed in a future version",
            DeprecationWarning,
            stacklevel=find_stack_level(inspect.currentframe()),
        )
        return {k: getattr(self, k, None) for k in self._attributes}
