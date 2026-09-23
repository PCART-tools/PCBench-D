    def __init__(self, block: Block, shape: Shape, indexers=None):
        # Passing shape explicitly is required for cases when block is None.
        # Note: block is None implies indexers is None, but not vice-versa
        if indexers is None:
            indexers = {}
        self.block = block
        self.indexers = indexers
        self.shape = shape
