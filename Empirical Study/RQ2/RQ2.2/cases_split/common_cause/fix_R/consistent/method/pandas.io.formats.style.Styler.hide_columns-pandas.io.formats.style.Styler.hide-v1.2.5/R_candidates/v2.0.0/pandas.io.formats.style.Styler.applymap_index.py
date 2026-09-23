    @doc(
        apply_index,
        this="applymap",
        wise="elementwise",
        alt="apply",
        altwise="level-wise",
        func="take a scalar and return a string",
        input_note="an index value, if an Index, or a level value of a MultiIndex",
        output_note="CSS styles as a string",
        var="v",
        ret='"background-color: yellow;" if v == "B" else None',
        ret2='"background-color: yellow;" if "x" in v else None',
    )
    def applymap_index(
        self,
        func: Callable,
        axis: AxisInt | str = 0,
        level: Level | list[Level] | None = None,
        **kwargs,
    ) -> Styler:
        self._todo.append(
            (
                lambda instance: getattr(instance, "_apply_index"),
                (func, axis, level, "applymap"),
                kwargs,
            )
        )
        return self
