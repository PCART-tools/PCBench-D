    def _draw_text_as_path(self, gc, x, y, s, prop, angle, ismath):
        # Implements the naive text drawing as is found in RendererBase.
        path, transform = self._get_text_path_transform(x, y, s, prop,
                                                        angle, ismath)
        color = gc.get_rgb()
        gc.set_linewidth(0.0)
        self.draw_path(gc, path, transform, rgbFace=color)
