    def __init__(self, elements: T.Sequence[Node], h: float = 0.0,
                 m: T.Literal['additional', 'exactly'] = 'additional'):
        super().__init__(elements)
        self.vpack(h=h, m=m)
