    @doc(NDFrame.interpolate, **_shared_docs_kwargs)
    def interpolate(
        self,
        method: QuantileInterpolation = "linear",
        *,
        axis: Axis = 0,
        limit=None,
        inplace: bool = False,
        limit_direction: Literal["forward", "backward", "both"] = "forward",
        limit_area=None,
        downcast=None,
        **kwargs,
    ):
        """
        Interpolate values according to different methods.
        """
        result = self._upsample("asfreq")
        return result.interpolate(
            method=method,
            axis=axis,
            limit=limit,
            inplace=inplace,
            limit_direction=limit_direction,
            limit_area=limit_area,
            downcast=downcast,
            **kwargs,
        )
