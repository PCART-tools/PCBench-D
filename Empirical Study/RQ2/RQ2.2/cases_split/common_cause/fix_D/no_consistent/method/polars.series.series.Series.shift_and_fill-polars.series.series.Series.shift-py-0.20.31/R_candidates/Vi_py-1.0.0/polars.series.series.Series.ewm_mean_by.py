    def ewm_mean_by(
        self,
        by: IntoExpr,
        *,
        half_life: str | timedelta,
    ) -> Series:
        r"""
        Calculate time-based exponentially weighted moving average.

        Given observations :math:`x_1, x_2, \ldots, x_n` at times
        :math:`t_1, t_2, \ldots, t_n`, the EWMA is calculated as

            .. math::

                y_0 &= x_0

                \alpha_i &= \exp(-\lambda(t_i - t_{i-1}))

                y_i &= \alpha_i x_i + (1 - \alpha_i) y_{i-1}; \quad i > 0

        where :math:`\lambda` equals :math:`\ln(2) / \text{half_life}`.

        Parameters
        ----------
        by
            Times to calculate average by. Should be ``DateTime``, ``Date``, ``UInt64``,
            ``UInt32``, ``Int64``, or ``Int32`` data type.
        half_life
            Unit over which observation decays to half its value.

            Can be created either from a timedelta, or
            by using the following string language:

            - 1ns   (1 nanosecond)
            - 1us   (1 microsecond)
            - 1ms   (1 millisecond)
            - 1s    (1 second)
            - 1m    (1 minute)
            - 1h    (1 hour)
            - 1d    (1 day)
            - 1w    (1 week)
            - 1i    (1 index count)

            Or combine them:
            "3d12h4m25s" # 3 days, 12 hours, 4 minutes, and 25 seconds

            Note that `half_life` is treated as a constant duration - calendar
            durations such as months (or even days in the time-zone-aware case)
            are not supported, please express your duration in an approximately
            equivalent number of hours (e.g. '370h' instead of '1mo').

        Returns
        -------
        Expr
            Float32 if input is Float32, otherwise Float64.

        Examples
        --------
        >>> from datetime import date, timedelta
        >>> df = pl.DataFrame(
        ...     {
        ...         "values": [0, 1, 2, None, 4],
        ...         "times": [
        ...             date(2020, 1, 1),
        ...             date(2020, 1, 3),
        ...             date(2020, 1, 10),
        ...             date(2020, 1, 15),
        ...             date(2020, 1, 17),
        ...         ],
        ...     }
        ... ).sort("times")
        >>> df["values"].ewm_mean_by(df["times"], half_life="4d")
        shape: (5,)
        Series: 'values' [f64]
        [
                0.0
                0.292893
                1.492474
                null
                3.254508
        ]
        """
