    def __init__(self, data, labels, ngroups, axis=0):
        self.data = data
        self.labels = ensure_int64(labels)
        self.ngroups = ngroups

        self.axis = axis
