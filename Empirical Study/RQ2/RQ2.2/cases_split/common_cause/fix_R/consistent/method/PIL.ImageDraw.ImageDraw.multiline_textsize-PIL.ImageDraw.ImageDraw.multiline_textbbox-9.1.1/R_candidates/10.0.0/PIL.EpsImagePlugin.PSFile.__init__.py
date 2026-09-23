    def __init__(self, fp):
        deprecate(
            "PSFile",
            11,
            action="If you need the functionality of this class "
            "you will need to implement it yourself.",
        )
        self.fp = fp
        self.char = None
