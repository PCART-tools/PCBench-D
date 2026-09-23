@_make_norm_from_scale(functools.partial(scale.LogScale, nonpositive="mask"))
class LogNorm(Normalize):
    """Normalize a given value to the 0-1 range on a log scale."""

    def autoscale(self, A):
        # docstring inherited.
        super().autoscale(np.ma.array(A, mask=(A <= 0)))

    def autoscale_None(self, A):
        # docstring inherited.
        super().autoscale_None(np.ma.array(A, mask=(A <= 0)))
