    def __init__(self, data, labels, ngroups, axis=0):
        super(NDFrameSplitter, self).__init__(data, labels, ngroups, axis=axis)

        self.factory = data._constructor
