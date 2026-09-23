    def __init__(self, inherited: str | None = None):
        if inherited is not None:
            self.inherited = self.compute_css(inherited)
        else:
            self.inherited = None
