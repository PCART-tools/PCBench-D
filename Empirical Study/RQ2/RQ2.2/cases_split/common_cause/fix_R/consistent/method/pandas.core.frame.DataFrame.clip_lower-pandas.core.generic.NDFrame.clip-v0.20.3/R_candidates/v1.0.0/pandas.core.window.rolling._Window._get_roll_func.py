    def _get_roll_func(self, func_name: str) -> Callable:
        """
        Wrap rolling function to check values passed.

        Parameters
        ----------
        func_name : str
            Cython function used to calculate rolling statistics

        Returns
        -------
        func : callable
        """
        window_func = getattr(window_aggregations, func_name, None)
        if window_func is None:
            raise ValueError(
                f"we do not support this function in window_aggregations.{func_name}"
            )
        return window_func
