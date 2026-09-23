    @staticmethod
    def _mpl_buttons():
        state = wx.GetMouseState()
        # NOTE: Alternatively, we could use event.LeftIsDown() / etc. but this
        # fails to report multiclick drags on macOS (other OSes have not been
        # verified).
        mod_table = [
            (MouseButton.LEFT, state.LeftIsDown()),
            (MouseButton.RIGHT, state.RightIsDown()),
            (MouseButton.MIDDLE, state.MiddleIsDown()),
            (MouseButton.BACK, state.Aux1IsDown()),
            (MouseButton.FORWARD, state.Aux2IsDown()),
        ]
        # State *after* press/release.
        return {button for button, flag in mod_table if flag}
