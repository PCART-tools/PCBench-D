    @final
    @doc(Expanding)
    def expanding(
        self,
        min_periods: int = 1,
        center: bool_t | None = None,
        axis: Axis = 0,
        method: str = "single",
    ) -> Expanding:
        axis = self._get_axis_number(axis)
        if center is not None:
            warnings.warn(
                "The `center` argument on `expanding` will be removed in the future.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
        else:
            center = False

        return Expanding(
            self, min_periods=min_periods, center=center, axis=axis, method=method
        )
