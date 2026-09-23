    def __init__(self, data: FrameOrSeries, labels, ngroups: int, axis: int = 0):
        self.data = data
        self.labels = ensure_int64(labels)
        self.ngroups = ngroups

        self.axis = axis
        assert isinstance(axis, int), axis
