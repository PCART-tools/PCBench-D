class Kern(Node):
    """
    A `Kern` node has a width field to specify a (normally
    negative) amount of spacing. This spacing correction appears in
    horizontal lists between letters like A and V when the font
    designer said that it looks better to move them closer together or
    further apart. A kern node can also appear in a vertical list,
    when its *width* denotes additional spacing in the vertical
    direction.
    """

    height = 0
    depth = 0

    def __init__(self, width):
        super().__init__()
        self.width = width

    def __repr__(self):
        return "k%.02f" % self.width

    def shrink(self):
        super().shrink()
        if self.size < NUM_SIZE_LEVELS:
            self.width *= SHRINK_FACTOR
