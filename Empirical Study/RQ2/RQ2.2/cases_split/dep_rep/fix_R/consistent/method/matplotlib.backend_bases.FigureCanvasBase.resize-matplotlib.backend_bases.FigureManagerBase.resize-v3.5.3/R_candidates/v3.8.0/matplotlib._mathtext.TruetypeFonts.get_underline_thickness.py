    def get_underline_thickness(self, font: str, fontsize: float, dpi: float) -> float:
        # This function used to grab underline thickness from the font
        # metrics, but that information is just too un-reliable, so it
        # is now hardcoded.
        return ((0.75 / 12.0) * fontsize * dpi) / 72.0
