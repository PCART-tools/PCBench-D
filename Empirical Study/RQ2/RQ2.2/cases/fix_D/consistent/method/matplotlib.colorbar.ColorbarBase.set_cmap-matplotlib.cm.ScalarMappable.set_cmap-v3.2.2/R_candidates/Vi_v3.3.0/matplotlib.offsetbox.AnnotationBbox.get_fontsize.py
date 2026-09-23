    @cbook._delete_parameter("3.3", "s")
    def get_fontsize(self, s=None):
        """Return the fontsize in points."""
        return self.prop.get_size_in_points()
