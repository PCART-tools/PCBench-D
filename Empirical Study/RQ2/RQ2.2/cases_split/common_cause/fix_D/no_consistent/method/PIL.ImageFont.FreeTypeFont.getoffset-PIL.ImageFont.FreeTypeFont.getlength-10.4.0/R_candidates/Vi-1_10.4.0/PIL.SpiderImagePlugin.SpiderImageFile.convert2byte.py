    def convert2byte(self, depth: int = 255) -> Image.Image:
        extrema = self.getextrema()
        assert isinstance(extrema[0], float)
        minimum, maximum = cast(Tuple[float, float], extrema)
        m: float = 1
        if maximum != minimum:
            m = depth / (maximum - minimum)
        b = -m * minimum
        return self.point(lambda i: i * m + b).convert("L")
