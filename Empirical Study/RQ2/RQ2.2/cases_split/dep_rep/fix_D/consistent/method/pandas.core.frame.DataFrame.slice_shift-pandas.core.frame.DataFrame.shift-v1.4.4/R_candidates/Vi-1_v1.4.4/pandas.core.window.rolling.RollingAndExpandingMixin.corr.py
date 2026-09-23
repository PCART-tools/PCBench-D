    def corr(
        self,
        other: DataFrame | Series | None = None,
        pairwise: bool | None = None,
        ddof: int = 1,
        **kwargs,
    ):

        from pandas import Series

        def corr_func(x, y):
            x_array = self._prep_values(x)
            y_array = self._prep_values(y)
            window_indexer = self._get_window_indexer()
            min_periods = (
                self.min_periods
                if self.min_periods is not None
                else window_indexer.window_size
            )
            start, end = window_indexer.get_window_bounds(
                num_values=len(x_array),
                min_periods=min_periods,
                center=self.center,
                closed=self.closed,
            )
            self._check_window_bounds(start, end, len(x_array))

            with np.errstate(all="ignore"):
                mean_x_y = window_aggregations.roll_mean(
                    x_array * y_array, start, end, min_periods
                )
                mean_x = window_aggregations.roll_mean(x_array, start, end, min_periods)
                mean_y = window_aggregations.roll_mean(y_array, start, end, min_periods)
                count_x_y = window_aggregations.roll_sum(
                    notna(x_array + y_array).astype(np.float64), start, end, 0
                )
                x_var = window_aggregations.roll_var(
                    x_array, start, end, min_periods, ddof
                )
                y_var = window_aggregations.roll_var(
                    y_array, start, end, min_periods, ddof
                )
                numerator = (mean_x_y - mean_x * mean_y) * (
                    count_x_y / (count_x_y - ddof)
                )
                denominator = (x_var * y_var) ** 0.5
                result = numerator / denominator
            return Series(result, index=x.index, name=x.name)

        return self._apply_pairwise(self._selected_obj, other, pairwise, corr_func)
