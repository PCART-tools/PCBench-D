    @Appender(get_window_bounds_doc)
    def get_window_bounds(
        self,
        num_values: int = 0,
        min_periods: int | None = None,
        center: bool | None = None,
        closed: str | None = None,
    ) -> tuple[np.ndarray, np.ndarray]:

        if center:
            raise ValueError("Forward-looking windows can't have center=True")
        if closed is not None:
            raise ValueError(
                "Forward-looking windows don't support setting the closed argument"
            )

        start = np.arange(num_values, dtype="int64")
        end = start + self.window_size
        if self.window_size:
            end[-self.window_size :] = num_values

        return start, end
