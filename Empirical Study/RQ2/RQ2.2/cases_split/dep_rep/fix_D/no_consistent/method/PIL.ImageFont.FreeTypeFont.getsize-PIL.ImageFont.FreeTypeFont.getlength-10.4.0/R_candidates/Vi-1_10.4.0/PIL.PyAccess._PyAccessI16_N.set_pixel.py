    def set_pixel(self, x, y, color):
        try:
            # integer
            self.pixels[y][x] = min(color, 65535)
        except TypeError:
            # tuple
            self.pixels[y][x] = min(color[0], 65535)
