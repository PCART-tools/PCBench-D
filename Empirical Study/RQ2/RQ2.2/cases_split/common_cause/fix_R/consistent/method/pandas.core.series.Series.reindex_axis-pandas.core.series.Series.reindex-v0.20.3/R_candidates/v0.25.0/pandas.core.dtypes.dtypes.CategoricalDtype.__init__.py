    def __init__(self, categories=None, ordered: OrderedType = ordered_sentinel):
        self._finalize(categories, ordered, fastpath=False)
