    def get_current_underline_thickness(self):
        """Return the underline thickness for this state."""
        return self.fontset.get_underline_thickness(
            self.font, self.fontsize, self.dpi)
