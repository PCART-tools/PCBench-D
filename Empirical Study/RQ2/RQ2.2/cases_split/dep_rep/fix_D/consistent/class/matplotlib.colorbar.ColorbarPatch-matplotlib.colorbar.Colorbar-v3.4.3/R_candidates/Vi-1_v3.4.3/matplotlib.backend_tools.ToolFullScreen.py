class ToolFullScreen(ToolToggleBase):
    """Tool to toggle full screen."""

    description = 'Toggle fullscreen mode'
    default_keymap = mpl.rcParams['keymap.fullscreen']

    def enable(self, event):
        self.figure.canvas.manager.full_screen_toggle()

    def disable(self, event):
        self.figure.canvas.manager.full_screen_toggle()
