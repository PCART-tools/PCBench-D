    def __call__(self, t):
        """
        Evaluate the Bezier curve at point(s) t in [0, 1].

        Parameters
        ----------
        t : float (k,), array_like
            Points at which to evaluate the curve.

        Returns
        -------
        float (k, d), array_like
            Value of the curve for each point in *t*.
        """
        t = np.asarray(t)
        return (np.power.outer(1 - t, self._orders[::-1])
                * np.power.outer(t, self._orders)) @ self._px
