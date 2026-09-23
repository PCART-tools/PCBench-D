    def __init__(self, radius: float | Sequence[float]) -> None:
        xy = radius if isinstance(radius, (tuple, list)) else (radius, radius)
        if xy[0] < 0 or xy[1] < 0:
            msg = "radius must be >= 0"
            raise ValueError(msg)
        self.radius = radius
