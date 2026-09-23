    @final
    def _make_wrapper(self, name: str) -> Callable:
        assert name in self._apply_allowlist

        with self._group_selection_context():
            # need to setup the selection
            # as are not passed directly but in the grouper
            f = getattr(self._obj_with_exclusions, name)
            if not isinstance(f, types.MethodType):
                #  error: Incompatible return value type
                # (got "NDFrameT", expected "Callable[..., Any]")  [return-value]
                return cast(Callable, self.apply(lambda self: getattr(self, name)))

        f = getattr(type(self._obj_with_exclusions), name)
        sig = inspect.signature(f)

        def wrapper(*args, **kwargs):
            # a little trickery for aggregation functions that need an axis
            # argument
            if "axis" in sig.parameters:
                if kwargs.get("axis", None) is None:
                    kwargs["axis"] = self.axis

            numeric_only = kwargs.get("numeric_only", lib.no_default)

            def curried(x):
                with warnings.catch_warnings():
                    # Catch any warnings from dispatch to DataFrame; we'll emit
                    # a warning for groupby below
                    match = "The default value of numeric_only "
                    warnings.filterwarnings("ignore", match, FutureWarning)
                    return f(x, *args, **kwargs)

            # preserve the name so we can detect it when calling plot methods,
            # to avoid duplicates
            curried.__name__ = name

            # special case otherwise extra plots are created when catching the
            # exception below
            if name in base.plotting_methods:
                return self.apply(curried)

            is_transform = name in base.transformation_kernels

            # Transform needs to keep the same schema, including when empty
            if is_transform and self._obj_with_exclusions.empty:
                return self._obj_with_exclusions

            result = self._python_apply_general(
                curried,
                self._obj_with_exclusions,
                is_transform=is_transform,
                not_indexed_same=not is_transform,
            )

            if self._selected_obj.ndim != 1 and self.axis != 1 and result.ndim != 1:
                missing = self._obj_with_exclusions.columns.difference(result.columns)
                if len(missing) > 0:
                    warn_dropping_nuisance_columns_deprecated(
                        type(self), name, numeric_only
                    )

            if self.grouper.has_dropped_na and is_transform:
                # result will have dropped rows due to nans, fill with null
                # and ensure index is ordered same as the input
                result = self._set_result_index_ordered(result)
            return result

        wrapper.__name__ = name
        return wrapper
