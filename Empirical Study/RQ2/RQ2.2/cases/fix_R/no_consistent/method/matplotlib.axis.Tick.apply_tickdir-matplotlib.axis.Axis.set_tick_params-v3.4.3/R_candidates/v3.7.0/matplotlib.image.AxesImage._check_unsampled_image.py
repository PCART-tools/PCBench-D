    def _check_unsampled_image(self):
        """Return whether the image would be better drawn unsampled."""
        return self.get_interpolation() == "none"
