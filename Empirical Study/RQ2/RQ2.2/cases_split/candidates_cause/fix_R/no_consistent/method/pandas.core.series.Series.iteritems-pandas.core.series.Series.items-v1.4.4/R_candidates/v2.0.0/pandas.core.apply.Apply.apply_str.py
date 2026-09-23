    def apply_str(self) -> DataFrame | Series:
        """
        Compute apply in case of a string.

        Returns
        -------
        result: Series or DataFrame
        """
        # Caller is responsible for checking isinstance(self.f, str)
        f = cast(str, self.f)

        obj = self.obj

        # Support for `frame.transform('method')`
        # Some methods (shift, etc.) require the axis argument, others
        # don't, so inspect and insert if necessary.
        func = getattr(obj, f, None)
        if callable(func):
            sig = inspect.getfullargspec(func)
            arg_names = (*sig.args, *sig.kwonlyargs)
            if self.axis != 0 and (
                "axis" not in arg_names or f in ("corrwith", "skew")
            ):
                raise ValueError(f"Operation {f} does not support axis=1")
            if "axis" in arg_names:
                self.kwargs["axis"] = self.axis
        return self._try_aggregate_string_function(obj, f, *self.args, **self.kwargs)
