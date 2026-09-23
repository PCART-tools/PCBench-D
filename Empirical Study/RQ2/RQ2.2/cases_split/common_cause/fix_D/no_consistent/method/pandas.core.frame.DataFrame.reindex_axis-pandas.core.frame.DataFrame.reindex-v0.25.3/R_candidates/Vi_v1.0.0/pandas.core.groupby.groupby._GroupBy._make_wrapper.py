    def _make_wrapper(self, name):
        assert name in self._apply_whitelist

        self._set_group_selection()

        # need to setup the selection
        # as are not passed directly but in the grouper
        f = getattr(self._selected_obj, name)
        if not isinstance(f, types.MethodType):
            return self.apply(lambda self: getattr(self, name))

        f = getattr(type(self._selected_obj), name)
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

            try:
                return self.apply(curried)
            except TypeError as err:
                if not re.search(
                    "reduction operation '.*' not allowed for this dtype", str(err)
                ):
                    # We don't have a cython implementation
                    # TODO: is the above comment accurate?
                    raise

            if self.obj.ndim == 1:
                # this can be called recursively, so need to raise ValueError
                raise ValueError

            # GH#3688 try to operate item-by-item
            result = self._aggregate_item_by_item(name, *args, **kwargs)
            return result

        wrapper.__name__ = name
        return wrapper
