    def _check_percentile(self, q):
        """
        Validate percentiles (used by describe and quantile).
        """

        msg = "percentiles should all be in the interval [0, 1]. " "Try {0} instead."
        q = np.asarray(q)
        if q.ndim == 0:
            if not 0 <= q <= 1:
                raise ValueError(msg.format(q / 100.0))
        else:
            if not all(0 <= qs <= 1 for qs in q):
                raise ValueError(msg.format(q / 100.0))
        return q
