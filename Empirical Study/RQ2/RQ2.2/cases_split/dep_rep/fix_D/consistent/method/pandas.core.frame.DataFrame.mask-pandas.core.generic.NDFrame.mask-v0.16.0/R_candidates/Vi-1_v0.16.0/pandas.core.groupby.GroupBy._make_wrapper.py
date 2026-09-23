    def _make_wrapper(self, name):
        if name not in self._apply_whitelist:
            is_callable = callable(getattr(self._selected_obj, name, None))
            kind = ' callable ' if is_callable else ' '
            msg = ("Cannot access{0}attribute {1!r} of {2!r} objects, try "
                   "using the 'apply' method".format(kind, name,
                                                     type(self).__name__))
            raise AttributeError(msg)

        # need to setup the selection
        # as are not passed directly but in the grouper
        self._set_selection_from_grouper()

        f = getattr(self._selected_obj, name)
        if not isinstance(f, types.MethodType):
            return self.apply(lambda self: getattr(self, name))

        f = getattr(type(self._selected_obj), name)

        def wrapper(*args, **kwargs):
            # a little trickery for aggregation functions that need an axis
            # argument
            kwargs_with_axis = kwargs.copy()
            if 'axis' not in kwargs_with_axis or kwargs_with_axis['axis']==None:
                kwargs_with_axis['axis'] = self.axis

            def curried_with_axis(x):
                return f(x, *args, **kwargs_with_axis)

            def curried(x):
                return f(x, *args, **kwargs)

            # preserve the name so we can detect it when calling plot methods,
            # to avoid duplicates
            curried.__name__ = curried_with_axis.__name__ = name

            # special case otherwise extra plots are created when catching the
            # exception below
            if name in _plotting_methods:
                return self.apply(curried)

            try:
                return self.apply(curried_with_axis)
            except Exception:
                try:
                    return self.apply(curried)
                except Exception:

                    # related to : GH3688
                    # try item-by-item
                    # this can be called recursively, so need to raise ValueError if
                    # we don't have this method to indicated to aggregate to
                    # mark this column as an error
                    try:
                        return self._aggregate_item_by_item(name, *args, **kwargs)
                    except (AttributeError):
                        raise ValueError

        return wrapper
