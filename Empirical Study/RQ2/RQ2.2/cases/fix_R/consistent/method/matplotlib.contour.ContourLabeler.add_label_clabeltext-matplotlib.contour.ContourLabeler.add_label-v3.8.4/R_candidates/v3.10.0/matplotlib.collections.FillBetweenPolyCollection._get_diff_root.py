    @staticmethod
    def _get_diff_root(x, xp, fp):
        """Calculate diff root."""
        order = xp.argsort()
        return np.interp(x, xp[order], fp[order])
