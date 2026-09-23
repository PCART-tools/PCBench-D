    def _check_unsampled_image(self, renderer):
        """
        return True if the image is better to be drawn unsampled.
        The derived class needs to override it.
        """
        return False
