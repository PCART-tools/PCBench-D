    def __init__(self, radius):
        if radius < 0:
            msg = "radius must be >= 0"
            raise ValueError(msg)
        self.radius = radius
