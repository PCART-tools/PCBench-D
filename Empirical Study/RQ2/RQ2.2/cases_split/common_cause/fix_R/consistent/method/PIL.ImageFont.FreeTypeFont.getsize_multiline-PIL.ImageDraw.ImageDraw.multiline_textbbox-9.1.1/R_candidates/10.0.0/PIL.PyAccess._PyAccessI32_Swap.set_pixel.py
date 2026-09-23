    def set_pixel(self, x, y, color):
        self.pixels[y][x] = self.reverse(color)
