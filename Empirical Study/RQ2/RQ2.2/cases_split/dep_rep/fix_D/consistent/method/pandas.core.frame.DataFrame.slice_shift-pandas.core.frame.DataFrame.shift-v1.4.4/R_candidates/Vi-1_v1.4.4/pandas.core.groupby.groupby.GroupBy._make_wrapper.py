    @final
    def _make_wrapper(self, name: str) -> Callable:
        assert name in self._apply_allowlist

        with self._group_selection_context():
            # need to setup the selection
            # as are not passed directly but in the grouper
            f = getattr(self._obj_with_exclusions, name)
            if not isinstance(f, types.MethodType):
                return self.apply(lambda self: getattr(self, name))

        f = getattr(type(self._obj_with_exclusions), name)
        sig = inspect.signature(f)

        def wrapper(*args, **kwargs):
            # a little trickery for aggregation functions that need an axis
            # argument
            if "axis" in sig.parameters:
                if kwargs.get("axis", None) is None:
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

            return self._python_apply_general(curried, self._obj_with_exclusions)

        wrapper.__name__ = name
        return wrapper
