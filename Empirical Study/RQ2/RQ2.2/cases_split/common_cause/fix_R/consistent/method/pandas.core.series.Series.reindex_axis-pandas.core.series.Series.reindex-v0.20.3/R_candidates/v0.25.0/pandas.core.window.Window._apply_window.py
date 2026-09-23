    def _apply_window(self, mean=True, **kwargs):
        """
        Applies a moving window of type ``window_type`` on the data.

        Parameters
        ----------
        mean : bool, default True
            If True computes weighted mean, else weighted sum

        Returns
        -------
        y : same type as input argument

        """
        window = self._prep_window(**kwargs)
        center = self.center

        blocks, obj = self._create_blocks()
        block_list = list(blocks)

        results = []
        exclude = []
        for i, b in enumerate(blocks):
            try:
                values = self._prep_values(b.values)

            except (TypeError, NotImplementedError):
                if isinstance(obj, ABCDataFrame):
                    exclude.extend(b.columns)
                    del block_list[i]
                    continue
                else:
                    raise DataError("No numeric types to aggregate")

            if values.size == 0:
                results.append(values.copy())
                continue

            offset = _offset(window, center)
            additional_nans = np.array([np.NaN] * offset)

            def f(arg, *args, **kwargs):
                minp = _use_window(self.min_periods, len(window))
                return libwindow.roll_window(
                    np.concatenate((arg, additional_nans)) if center else arg,
                    window,
                    minp,
                    avg=mean,
                )

            result = np.apply_along_axis(f, self.axis, values)

            if center:
                result = self._center_window(result, window)
            results.append(result)

        return self._wrap_results(results, block_list, obj, exclude)
