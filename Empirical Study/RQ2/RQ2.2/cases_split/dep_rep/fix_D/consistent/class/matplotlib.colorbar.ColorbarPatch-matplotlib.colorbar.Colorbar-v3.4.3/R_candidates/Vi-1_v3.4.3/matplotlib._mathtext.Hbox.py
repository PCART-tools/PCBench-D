class Hbox(Box):
    """A box with only width (zero height and depth)."""

    def __init__(self, width):
        super().__init__(width, 0., 0.)
