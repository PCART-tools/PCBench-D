    def update_positions(self, renderer):
        """
        Update the pixel positions of the annotated point and the text.
        """
        xy_pixel = self._get_position_xy(renderer)
        self._update_position_xybox(renderer, xy_pixel)

        mutation_scale = renderer.points_to_pixels(self.get_fontsize())
        self.patch.set_mutation_scale(mutation_scale)

        if self.arrow_patch:
            self.arrow_patch.set_mutation_scale(mutation_scale)
