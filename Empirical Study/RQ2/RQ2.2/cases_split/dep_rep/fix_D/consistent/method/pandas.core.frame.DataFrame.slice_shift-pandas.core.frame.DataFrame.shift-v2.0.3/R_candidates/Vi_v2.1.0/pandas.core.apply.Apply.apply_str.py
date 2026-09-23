    def apply_str(self) -> DataFrame | Series:
        """
        Compute apply in case of a string.

        Returns
        -------
        result: Series or DataFrame
        """
        # Caller is responsible for checking isinstance(self.f, str)
        func = cast(str, self.func)

        obj = self.obj

        from pandas.core.groupby.generic import (
            DataFrameGroupBy,
            SeriesGroupBy,
        )

        # Support for `frame.transform('method')`
        # Some methods (shift, etc.) require the axis argument, others
        # don't, so inspect and insert if necessary.
        method = getattr(obj, func, None)
        if callable(method):
            sig = inspect.getfullargspec(method)
            arg_names = (*sig.args, *sig.kwonlyargs)
            if self.axis != 0 and (
                "axis" not in arg_names or func in ("corrwith", "skew")
            ):
                raise ValueError(f"Operation {func} does not support axis=1")
            if "axis" in arg_names:
                if isinstance(obj, (SeriesGroupBy, DataFrameGroupBy)):
                    # Try to avoid FutureWarning for deprecated axis keyword;
                    # If self.axis matches the axis we would get by not passing
                    #  axis, we safely exclude the keyword.

                    default_axis = 0
                    if func in ["idxmax", "idxmin"]:
                        # DataFrameGroupBy.idxmax, idxmin axis defaults to self.axis,
                        # whereas other axis keywords default to 0
                        default_axis = self.obj.axis

                    if default_axis != self.axis:
                        self.kwargs["axis"] = self.axis
                else:
                    self.kwargs["axis"] = self.axis
        return self._apply_str(obj, func, *self.args, **self.kwargs)
