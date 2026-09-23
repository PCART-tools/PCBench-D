    def get_underline_thickness(self, font: str, fontsize: float, dpi: float) -> float:
        """
        Get the line thickness that matches the given font.  Used as a
        base unit for drawing lines such as in a fraction or radical.
        """
        raise NotImplementedError()
