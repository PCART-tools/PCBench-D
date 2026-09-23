    @final
    @doc(Expanding)
    def expanding(
        self,
        min_periods: int = 1,
        axis: Axis | lib.NoDefault = lib.no_default,
        method: Literal["single", "table"] = "single",
    ) -> Expanding:
        if axis is not lib.no_default:
            axis = self._get_axis_number(axis)
            name = "expanding"
            if axis == 1:
                warnings.warn(
                    f"Support for axis=1 in {type(self).__name__}.{name} is "
                    "deprecated and will be removed in a future version. "
                    f"Use obj.T.{name}(...) instead",
                    FutureWarning,
                    stacklevel=find_stack_level(),
                )
            else:
                warnings.warn(
                    f"The 'axis' keyword in {type(self).__name__}.{name} is "
                    "deprecated and will be removed in a future version. "
                    "Call the method without the axis keyword instead.",
                    FutureWarning,
                    stacklevel=find_stack_level(),
                )
        else:
            axis = 0
        return Expanding(self, min_periods=min_periods, axis=axis, method=method)
