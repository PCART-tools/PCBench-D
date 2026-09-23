    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        """
        Render the text
        """
        if ismath:
            return self.draw_mathtext(gc, x, y, s, prop, angle)

        flags = get_hinting_flag()
        font = self._get_agg_font(prop)

        if font is None:
            return None
        if len(s) == 1 and ord(s) > 127:
            font.load_char(ord(s), flags=flags)
        else:
            # We pass '0' for angle here, since it will be rotated (in raster
            # space) in the following call to draw_text_image).
            font.set_text(s, 0, flags=flags)
        font.draw_glyphs_to_bitmap(antialiased=rcParams['text.antialiased'])
        d = font.get_descent() / 64.0
        # The descent needs to be adjusted for the angle
        xo, yo = font.get_bitmap_offset()
        xo /= 64.0
        yo /= 64.0
        xd = -d * sin(radians(angle))
        yd = d * cos(radians(angle))

        #print x, y, int(x), int(y), s
        self._renderer.draw_text_image(
            font, np.round(x - xd + xo), np.round(y + yd + yo) + 1, angle, gc)
