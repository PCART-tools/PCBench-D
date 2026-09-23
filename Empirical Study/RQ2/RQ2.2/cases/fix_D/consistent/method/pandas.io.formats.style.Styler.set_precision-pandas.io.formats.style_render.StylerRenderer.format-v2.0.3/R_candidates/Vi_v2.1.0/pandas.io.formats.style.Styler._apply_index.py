    def _apply_index(
        self,
        func: Callable,
        axis: Axis = 0,
        level: Level | list[Level] | None = None,
        method: str = "apply",
        **kwargs,
    ) -> Styler:
        axis = self.data._get_axis_number(axis)
        obj = self.index if axis == 0 else self.columns

        levels_ = refactor_levels(level, obj)
        data = DataFrame(obj.to_list()).loc[:, levels_]

        if method == "apply":
            result = data.apply(func, axis=0, **kwargs)
        elif method == "map":
            result = data.map(func, **kwargs)

        self._update_ctx_header(result, axis)
        return self
