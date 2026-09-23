    def _draw_bbox(self, renderer, posx, posy):
        """
        Update the location and size of the bbox (`.patches.FancyBboxPatch`),
        and draw.
        """

        x_box, y_box, w_box, h_box = _get_textbox(self, renderer)
        self._bbox_patch.set_bounds(0., 0., w_box, h_box)
        theta = np.deg2rad(self.get_rotation())
        tr = Affine2D().rotate(theta)
        tr = tr.translate(posx + x_box, posy + y_box)
        self._bbox_patch.set_transform(tr)
        fontsize_in_pixel = renderer.points_to_pixels(self.get_size())
        self._bbox_patch.set_mutation_scale(fontsize_in_pixel)
        self._bbox_patch.draw(renderer)
