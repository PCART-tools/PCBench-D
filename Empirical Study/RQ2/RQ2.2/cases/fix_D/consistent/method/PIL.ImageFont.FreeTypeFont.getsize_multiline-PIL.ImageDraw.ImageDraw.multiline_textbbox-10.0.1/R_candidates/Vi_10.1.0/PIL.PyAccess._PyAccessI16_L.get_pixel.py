    def get_pixel(self, x, y):
        pixel = self.pixels[y][x]
        return pixel.l + pixel.r * 256
