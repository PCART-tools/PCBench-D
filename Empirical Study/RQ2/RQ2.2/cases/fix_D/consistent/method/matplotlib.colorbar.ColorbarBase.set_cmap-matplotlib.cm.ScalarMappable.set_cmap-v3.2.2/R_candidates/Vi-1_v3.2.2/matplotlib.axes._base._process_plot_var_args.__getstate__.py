    def __getstate__(self):
        # note: it is not possible to pickle a generator (and thus a cycler).
        return {'axes': self.axes, 'command': self.command}
