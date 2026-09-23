    def _apply(self, func, **kwargs):
        """
        Rolling statistical measure using supplied function. Designed to be
        used with passed-in Cython array-based functions.

        Parameters
        ----------
        func : str/callable to apply

        Returns
        -------
        y : same type as input argument
        """
        blocks, obj, index = self._create_blocks()
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
                cfunc = getattr(libwindow, func, None)
                if cfunc is None:
                    raise ValueError("we do not support this function "
                                     "in libwindow.{func}".format(func=func))

                def func(arg):
                    return cfunc(arg, self.com, int(self.adjust),
                                 int(self.ignore_na), int(self.min_periods))

            results.append(np.apply_along_axis(func, self.axis, values))

        return self._wrap_results(results, blocks, obj)
