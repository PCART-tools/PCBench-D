    def update_bbox_position_size(self, renderer):
        """
        Update the location and the size of the bbox. This method
        should be used when the position and size of the bbox needs to
        be updated before actually drawing the bbox.
        """

        if self._bbox_patch:

            trans = self.get_transform()

            # don't use self.get_unitless_position here, which refers to text
            # position in Text, and dash position in TextWithDash:
            posx = float(self.convert_xunits(self._x))
            posy = float(self.convert_yunits(self._y))

            posx, posy = trans.transform_point((posx, posy))

            x_box, y_box, w_box, h_box = _get_textbox(self, renderer)
            self._bbox_patch.set_bounds(0., 0., w_box, h_box)
            theta = np.deg2rad(self.get_rotation())
            tr = mtransforms.Affine2D().rotate(theta)
            tr = tr.translate(posx + x_box, posy + y_box)
            self._bbox_patch.set_transform(tr)
            fontsize_in_pixel = renderer.points_to_pixels(self.get_size())
            self._bbox_patch.set_mutation_scale(fontsize_in_pixel)
