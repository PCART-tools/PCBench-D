    def __hash__(self):
        # Python3 doesn't inherit __hash__ when a base class overrides
        # __eq__, so we explicitly do it here.
        return super(SparseDtype, self).__hash__()
