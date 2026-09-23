    def _check_unsampled_image(self, renderer):
        """
        Return whether the image is better to be drawn unsampled.

        The derived class needs to override it.
        """
        return False
