    def get_pixel(self, x: int, y: int) -> int:
        pixel = self.pixels[y][x]
        return pixel.l * 256 + pixel.r
