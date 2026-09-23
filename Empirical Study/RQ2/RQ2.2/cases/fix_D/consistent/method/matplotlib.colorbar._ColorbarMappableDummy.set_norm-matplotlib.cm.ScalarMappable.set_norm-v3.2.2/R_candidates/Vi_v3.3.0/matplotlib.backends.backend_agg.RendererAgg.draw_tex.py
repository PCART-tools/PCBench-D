    @cbook._delete_parameter("3.2", "ismath")
    def draw_tex(self, gc, x, y, s, prop, angle, ismath='TeX!', mtext=None):
        # docstring inherited
        # todo, handle props, angle, origins
        size = prop.get_size_in_points()

        texmanager = self.get_texmanager()

        Z = texmanager.get_grey(s, size, self.dpi)
        Z = np.array(Z * 255.0, np.uint8)

        w, h, d = self.get_text_width_height_descent(s, prop, ismath="TeX")
        xd = d * sin(radians(angle))
        yd = d * cos(radians(angle))
        x = round(x + xd)
        y = round(y + yd)
        self._renderer.draw_text_image(Z, x, y, angle, gc)
