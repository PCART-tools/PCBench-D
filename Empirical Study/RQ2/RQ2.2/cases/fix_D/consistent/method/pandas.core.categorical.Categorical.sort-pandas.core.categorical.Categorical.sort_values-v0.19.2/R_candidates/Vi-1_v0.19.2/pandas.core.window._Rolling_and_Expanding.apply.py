    def apply(self, func, args=(), kwargs={}):
        # TODO: _level is unused?
        _level = kwargs.pop('_level', None)  # noqa
        window = self._get_window()
        offset = _offset(window, self.center)
        index, indexi = self._get_index()

        def f(arg, window, min_periods):
            minp = _use_window(min_periods, window)
            return _window.roll_generic(arg, window, minp, indexi,
                                        offset, func, args,
                                        kwargs)

        return self._apply(f, func, args=args, kwargs=kwargs,
                           center=False)
