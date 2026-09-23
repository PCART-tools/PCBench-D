    def __init__(self, categories=None, ordered: Ordered = False):
        self._finalize(categories, ordered, fastpath=False)
