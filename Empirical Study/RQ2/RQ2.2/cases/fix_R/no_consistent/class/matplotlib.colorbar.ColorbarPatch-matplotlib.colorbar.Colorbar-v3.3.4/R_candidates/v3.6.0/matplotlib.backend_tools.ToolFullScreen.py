class ToolFullScreen(ToolBase):
    """Tool to toggle full screen."""

    description = 'Toggle fullscreen mode'
    default_keymap = property(lambda self: mpl.rcParams['keymap.fullscreen'])

    def trigger(self, sender, event, data=None):
        self.figure.canvas.manager.full_screen_toggle()
