    def __array_ufunc__(self, ufunc, method: str, *inputs, **kwargs):
        # Lightly modified version of
        # https://numpy.org/doc/stable/reference/generated/numpy.lib.mixins.NDArrayOperatorsMixin.html
        # The primary modification is not boxing scalar return values
        # in PandasArray, since pandas' ExtensionArrays are 1-d.
        out = kwargs.get("out", ())
        for x in inputs + out:
            # Only support operations with instances of _HANDLED_TYPES.
            # Use PandasArray instead of type(self) for isinstance to
            # allow subclasses that don't override __array_ufunc__ to
            # handle PandasArray objects.
            if not isinstance(x, self._HANDLED_TYPES + (PandasArray,)):
                return NotImplemented

        # Defer to the implementation of the ufunc on unwrapped values.
        inputs = tuple(x._ndarray if isinstance(x, PandasArray) else x for x in inputs)
        if out:
            kwargs["out"] = tuple(
                x._ndarray if isinstance(x, PandasArray) else x for x in out
            )
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple and len(result):
            # multiple return values
            if not lib.is_scalar(result[0]):
                # re-box array-like results
                return tuple(type(self)(x) for x in result)
            else:
                # but not scalar reductions
                return result
        elif method == "at":
            # no return value
            return None
        else:
            # one return value
            if not lib.is_scalar(result):
                # re-box array-like results, but not scalar reductions
                result = type(self)(result)
            return result
