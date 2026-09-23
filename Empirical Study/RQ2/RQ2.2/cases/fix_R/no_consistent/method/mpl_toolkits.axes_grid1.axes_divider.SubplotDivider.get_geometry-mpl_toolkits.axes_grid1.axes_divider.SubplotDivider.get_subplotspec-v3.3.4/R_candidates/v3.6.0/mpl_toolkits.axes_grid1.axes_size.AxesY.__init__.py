    def __init__(self, axes, aspect=1., ref_ax=None):
        self._axes = axes
        self._aspect = aspect
        if aspect == "axes" and ref_ax is None:
            raise ValueError("ref_ax must be set when aspect='axes'")
        self._ref_ax = ref_ax
