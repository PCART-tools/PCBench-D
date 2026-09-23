    def _apply_window(self, mean=True, **kwargs):
        """
        Applies a moving window of type ``window_type`` on the data.

        Parameters
        ----------
        mean : boolean, default True
            If True computes weighted mean, else weighted sum

        Returns
        -------
        y : type of input argument

        """
        window = self._prep_window(**kwargs)
        center = self.center

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

            offset = _offset(window, center)
            additional_nans = np.array([np.NaN] * offset)

            def f(arg, *args, **kwargs):
                minp = _use_window(self.min_periods, len(window))
                return _window.roll_window(np.concatenate((arg,
                                                           additional_nans))
                                           if center else arg, window, minp,
                                           avg=mean)

            result = np.apply_along_axis(f, self.axis, values)

            if center:
                result = self._center_window(result, window)
            results.append(result)

        return self._wrap_results(results, blocks, obj)
