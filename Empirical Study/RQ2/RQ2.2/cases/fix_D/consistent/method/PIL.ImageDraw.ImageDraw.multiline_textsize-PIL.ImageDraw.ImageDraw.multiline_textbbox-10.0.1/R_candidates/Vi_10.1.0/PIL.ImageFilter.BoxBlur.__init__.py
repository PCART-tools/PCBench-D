    def __init__(self, radius):
        xy = radius
        if not isinstance(xy, (tuple, list)):
            xy = (xy, xy)
        if xy[0] < 0 or xy[1] < 0:
            msg = "radius must be >= 0"
            raise ValueError(msg)
        self.radius = radius
