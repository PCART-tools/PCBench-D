    def __init__(self, key=None, level=None, freq=None, axis=0, sort=False):
        self.key=key
        self.level=level
        self.freq=freq
        self.axis=axis
        self.sort=sort

        self.grouper=None
        self.obj=None
        self.indexer=None
        self.binner=None
        self.grouper=None
