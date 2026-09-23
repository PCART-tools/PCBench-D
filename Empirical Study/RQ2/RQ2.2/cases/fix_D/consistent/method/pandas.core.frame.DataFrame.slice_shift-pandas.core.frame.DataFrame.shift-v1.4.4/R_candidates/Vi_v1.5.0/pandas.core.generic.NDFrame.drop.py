    @deprecate_nonkeyword_arguments(version=None, allowed_args=["self", "labels"])
    def drop(
        self: NDFrameT,
        labels: IndexLabel = None,
        axis: Axis = 0,
        index: IndexLabel = None,
        columns: IndexLabel = None,
        level: Level | None = None,
        inplace: bool_t = False,
        errors: IgnoreRaise = "raise",
    ) -> NDFrameT | None:

        inplace = validate_bool_kwarg(inplace, "inplace")

        if labels is not None:
            if index is not None or columns is not None:
                raise ValueError("Cannot specify both 'labels' and 'index'/'columns'")
            axis_name = self._get_axis_name(axis)
            axes = {axis_name: labels}
        elif index is not None or columns is not None:
            axes, _ = self._construct_axes_from_arguments((index, columns), {})
        else:
            raise ValueError(
                "Need to specify at least one of 'labels', 'index' or 'columns'"
            )

        obj = self

        for axis, labels in axes.items():
            if labels is not None:
                obj = obj._drop_axis(labels, axis, level=level, errors=errors)

        if inplace:
            self._update_inplace(obj)
        else:
            return obj
