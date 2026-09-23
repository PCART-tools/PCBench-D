    def __init__(self, state, thickness=None):
        if thickness is None:
            thickness = state.get_current_underline_thickness()
        height = depth = thickness * 0.5
        super().__init__(np.inf, height, depth, state)
