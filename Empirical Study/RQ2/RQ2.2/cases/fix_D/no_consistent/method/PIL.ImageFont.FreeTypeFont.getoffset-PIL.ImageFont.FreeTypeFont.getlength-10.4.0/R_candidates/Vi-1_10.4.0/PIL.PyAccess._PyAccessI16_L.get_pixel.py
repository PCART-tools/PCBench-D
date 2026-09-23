    def get_pixel(self, x: int, y: int) -> int:
        pixel = self.pixels[y][x]
        return pixel.l + pixel.r * 256
