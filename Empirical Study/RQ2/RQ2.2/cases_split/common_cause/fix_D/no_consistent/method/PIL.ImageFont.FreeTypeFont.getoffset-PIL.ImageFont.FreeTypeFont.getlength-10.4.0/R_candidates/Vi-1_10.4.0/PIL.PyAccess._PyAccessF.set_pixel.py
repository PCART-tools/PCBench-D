    def set_pixel(self, x, y, color):
        try:
            # not a tuple
            self.pixels[y][x] = color
        except TypeError:
            # tuple
            self.pixels[y][x] = color[0]
