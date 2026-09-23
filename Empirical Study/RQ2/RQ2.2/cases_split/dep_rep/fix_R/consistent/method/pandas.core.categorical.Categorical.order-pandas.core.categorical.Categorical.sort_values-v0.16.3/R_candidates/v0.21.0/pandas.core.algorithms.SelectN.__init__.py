    def __init__(self, obj, n, keep):
        self.obj = obj
        self.n = n
        self.keep = keep

        if self.keep not in ('first', 'last'):
            raise ValueError('keep must be either "first", "last"')
