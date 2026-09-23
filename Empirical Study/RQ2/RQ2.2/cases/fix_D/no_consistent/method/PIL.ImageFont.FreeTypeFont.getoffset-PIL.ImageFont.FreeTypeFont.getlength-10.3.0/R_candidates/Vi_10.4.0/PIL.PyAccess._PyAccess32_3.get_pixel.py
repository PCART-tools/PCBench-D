    def get_pixel(self, x: int, y: int) -> tuple[int, int, int]:
        pixel = self.pixels[y][x]
        return pixel.r, pixel.g, pixel.b
