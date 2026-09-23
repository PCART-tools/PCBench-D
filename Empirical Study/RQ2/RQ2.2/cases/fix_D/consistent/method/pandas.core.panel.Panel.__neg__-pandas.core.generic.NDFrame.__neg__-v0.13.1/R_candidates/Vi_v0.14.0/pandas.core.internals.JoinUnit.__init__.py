    def __init__(self, block, shape, indexers={}):
        # Passing shape explicitly is required for cases when block is None.
        self.block = block
        self.indexers = indexers
        self.shape = shape
