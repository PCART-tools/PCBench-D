    def __init__(self, categories=None, ordered: Ordered = False) -> None:
        self._finalize(categories, ordered, fastpath=False)
