    def _get_cython_function(self, kind: str, how: str, values, is_numeric: bool):

        dtype_str = values.dtype.name
        ftype = self._cython_functions[kind][how]

        # see if there is a fused-type version of function
        # only valid for numeric
        f = getattr(libgroupby, ftype, None)
        if f is not None and is_numeric:
            return f

        # otherwise find dtype-specific version, falling back to object
        for dt in [dtype_str, "object"]:
            f2 = getattr(libgroupby, f"{ftype}_{dt}", None)
            if f2 is not None:
                return f2

        if hasattr(f, "__signatures__"):
            # inspect what fused types are implemented
            if dtype_str == "object" and "object" not in f.__signatures__:
                # disallow this function so we get a NotImplementedError below
                #  instead of a TypeError at runtime
                f = None

        func = f

        if func is None:
            raise NotImplementedError(
                f"function is not implemented for this dtype: "
                f"[how->{how},dtype->{dtype_str}]"
            )

        return func
