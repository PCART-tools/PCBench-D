    def __getstate__(self):
        # store a dictionary of this SilentList's state
        return {'type': self.type, 'seq': self[:]}
