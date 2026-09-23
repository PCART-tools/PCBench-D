class Vbox(Box):
    """A box with only height (zero width)."""

    def __init__(self, height, depth):
        super().__init__(0., height, depth)
