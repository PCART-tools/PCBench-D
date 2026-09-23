    def get_pixel(self, x, y):
        pixel = self.pixels[y][x]
        return pixel.r, pixel.g, pixel.b
