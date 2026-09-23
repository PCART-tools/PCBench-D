    def __init__(self, width: float, height: float, depth: float, state: ParserState):
        super().__init__(width, height, depth)
        self.fontset = state.fontset
