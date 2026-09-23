    def __init__(self, elements: T.Sequence[Node], w: float = 0.0,
                 m: T.Literal['additional', 'exactly'] = 'additional',
                 do_kern: bool = True):
        super().__init__(elements)
        if do_kern:
            self.kern()
        self.hpack(w=w, m=m)
