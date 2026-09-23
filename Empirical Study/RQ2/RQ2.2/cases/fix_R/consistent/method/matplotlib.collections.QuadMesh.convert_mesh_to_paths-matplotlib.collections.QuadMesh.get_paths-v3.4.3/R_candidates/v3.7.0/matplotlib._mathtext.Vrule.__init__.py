    def __init__(self, state):
        thickness = state.get_current_underline_thickness()
        super().__init__(thickness, np.inf, np.inf, state)
