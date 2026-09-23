    def _check_unsampled_image(self, renderer):
        """
        Return whether the image would be better drawn unsampled.
        """
        return (self.get_interpolation() == "none"
                and renderer.option_scale_image())
