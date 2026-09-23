    def __getstate__(self):
        # note: it is not possible to pickle a itertools.cycle instance
        return {'axes': self.axes, 'command': self.command}
