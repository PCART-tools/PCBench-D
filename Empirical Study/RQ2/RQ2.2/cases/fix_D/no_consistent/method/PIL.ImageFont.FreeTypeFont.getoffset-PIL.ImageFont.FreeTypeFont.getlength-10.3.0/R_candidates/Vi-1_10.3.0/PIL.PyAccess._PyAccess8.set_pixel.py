    def set_pixel(self, x, y, color):
        try:
            # integer
            self.pixels[y][x] = min(color, 255)
        except TypeError:
            # tuple
            self.pixels[y][x] = min(color[0], 255)
