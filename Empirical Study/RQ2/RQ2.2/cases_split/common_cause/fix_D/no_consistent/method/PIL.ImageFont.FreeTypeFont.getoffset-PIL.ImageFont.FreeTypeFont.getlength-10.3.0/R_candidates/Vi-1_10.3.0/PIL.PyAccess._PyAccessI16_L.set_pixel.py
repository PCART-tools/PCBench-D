    def set_pixel(self, x, y, color):
        pixel = self.pixels[y][x]
        try:
            color = min(color, 65535)
        except TypeError:
            color = min(color[0], 65535)

        pixel.l = color & 0xFF
        pixel.r = color >> 8
