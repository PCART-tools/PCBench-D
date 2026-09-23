    def _info_repr(self):
        """True if the repr should show the info view."""
        info_repr_option = (get_option("display.large_repr") == "info")
        return info_repr_option and not (self._repr_fits_horizontal_() and
                                         self._repr_fits_vertical_())
