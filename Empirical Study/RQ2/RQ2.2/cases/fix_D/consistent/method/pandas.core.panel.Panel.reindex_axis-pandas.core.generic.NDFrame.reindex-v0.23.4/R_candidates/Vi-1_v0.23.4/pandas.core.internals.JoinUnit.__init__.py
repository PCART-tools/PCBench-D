    def __init__(self, block, shape, indexers=None):
        # Passing shape explicitly is required for cases when block is None.
        if indexers is None:
            indexers = {}
        self.block = block
        self.indexers = indexers
        self.shape = shape
