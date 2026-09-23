    def get_pixel(self, x: int, y: int) -> tuple[int, int]:
        pixel = self.pixels[y][x]
        return pixel.r, pixel.a
