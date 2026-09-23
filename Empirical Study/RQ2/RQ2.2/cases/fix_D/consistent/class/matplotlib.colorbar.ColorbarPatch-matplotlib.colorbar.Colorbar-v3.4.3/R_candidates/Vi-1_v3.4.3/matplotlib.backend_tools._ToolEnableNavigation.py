class _ToolEnableNavigation(ToolBase):
    """Tool to enable a specific axes for toolmanager interaction."""

    description = 'Enable one axes toolmanager'
    default_keymap = ('1', '2', '3', '4', '5', '6', '7', '8', '9')

    def trigger(self, sender, event, data=None):
        mpl.backend_bases.key_press_handler(event, self.figure.canvas, None)
