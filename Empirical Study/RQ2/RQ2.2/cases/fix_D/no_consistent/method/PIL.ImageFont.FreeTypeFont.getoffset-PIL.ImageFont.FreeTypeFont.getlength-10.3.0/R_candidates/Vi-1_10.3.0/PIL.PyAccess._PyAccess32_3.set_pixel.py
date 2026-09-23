    def set_pixel(self, x, y, color):
        pixel = self.pixels[y][x]
        # tuple
        pixel.r = min(color[0], 255)
        pixel.g = min(color[1], 255)
        pixel.b = min(color[2], 255)
        pixel.a = 255
