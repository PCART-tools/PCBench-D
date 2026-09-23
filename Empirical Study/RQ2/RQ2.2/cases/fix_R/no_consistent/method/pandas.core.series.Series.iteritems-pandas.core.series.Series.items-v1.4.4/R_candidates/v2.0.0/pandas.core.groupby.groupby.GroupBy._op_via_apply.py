    @final
    def _op_via_apply(self, name: str, *args, **kwargs):
        """Compute the result of an operation by using GroupBy's apply."""
        f = getattr(type(self._obj_with_exclusions), name)
        sig = inspect.signature(f)

        # a little trickery for aggregation functions that need an axis
        # argument
        if "axis" in sig.parameters:
            if kwargs.get("axis", None) is None or kwargs.get("axis") is lib.no_default:
                kwargs["axis"] = self.axis

        def curried(x):
            return f(x, *args, **kwargs)

        # preserve the name so we can detect it when calling plot methods,
        # to avoid duplicates
        curried.__name__ = name

        # special case otherwise extra plots are created when catching the
        # exception below
        if name in base.plotting_methods:
            return self.apply(curried)

        is_transform = name in base.transformation_kernels
        result = self._python_apply_general(
            curried,
            self._obj_with_exclusions,
            is_transform=is_transform,
            not_indexed_same=not is_transform,
        )

        if self.grouper.has_dropped_na and is_transform:
            # result will have dropped rows due to nans, fill with null
            # and ensure index is ordered same as the input
            result = self._set_result_index_ordered(result)
        return result
