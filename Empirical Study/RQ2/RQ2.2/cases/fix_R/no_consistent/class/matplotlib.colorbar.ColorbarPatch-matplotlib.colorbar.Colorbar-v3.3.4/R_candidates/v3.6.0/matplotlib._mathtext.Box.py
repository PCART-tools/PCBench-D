class Box(Node):
    """A node with a physical location."""

    def __init__(self, width, height, depth):
        super().__init__()
        self.width  = width
        self.height = height
        self.depth  = depth

    def shrink(self):
        super().shrink()
        if self.size < NUM_SIZE_LEVELS:
            self.width  *= SHRINK_FACTOR
            self.height *= SHRINK_FACTOR
            self.depth  *= SHRINK_FACTOR

    def render(self, output, x1, y1, x2, y2):
        pass
