    def __init__(self, state, thickness=None):
        if thickness is None:
            thickness = state.font_output.get_underline_thickness(
                state.font, state.fontsize, state.dpi)
        height = depth = thickness * 0.5
        Rule.__init__(self, np.inf, height, depth, state)
