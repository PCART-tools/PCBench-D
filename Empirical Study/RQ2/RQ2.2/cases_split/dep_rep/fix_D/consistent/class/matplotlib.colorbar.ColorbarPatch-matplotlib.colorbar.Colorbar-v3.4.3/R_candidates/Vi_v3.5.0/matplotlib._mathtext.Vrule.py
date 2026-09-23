class Vrule(Rule):
    """Convenience class to create a vertical rule."""

    def __init__(self, state):
        thickness = state.font_output.get_underline_thickness(
            state.font, state.fontsize, state.dpi)
        super().__init__(thickness, np.inf, np.inf, state)
