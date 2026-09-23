    def __init__(self, box: Box):
        self.box = box
        self.glyphs: list[tuple[float, float, FontInfo]] = []  # (ox, oy, info)
        self.rects: list[tuple[float, float, float, float]] = []  # (x1, y1, x2, y2)
