    def _apply(self, func, how=None, **kwargs):
        """Rolling statistical measure using supplied function. Designed to be
        used with passed-in Cython array-based functions.

        Parameters
        ----------
        func : string/callable to apply
        how : string, default to None
            .. deprecated:: 0.18.0
               how to resample

        Returns
        -------
        y : type of input argument

        """
        blocks, obj, index = self._create_blocks(how=how)
        results = []
        for b in blocks:
            try:
                values = self._prep_values(b.values)
            except TypeError:
                results.append(b.values.copy())
                continue

            if values.size == 0:
                results.append(values.copy())
                continue

            # if we have a string function name, wrap it
            if isinstance(func, compat.string_types):
                cfunc = getattr(_window, func, None)
                if cfunc is None:
                    raise ValueError("we do not support this function "
                                     "in _window.{0}".format(func))

                def func(arg):
                    return cfunc(arg, self.com, int(self.adjust),
                                 int(self.ignore_na), int(self.min_periods))

            results.append(np.apply_along_axis(func, self.axis, values))

        return self._wrap_results(results, blocks, obj)
