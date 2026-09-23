class _ToolEnableAllNavigation(ToolBase):
    """Tool to enable all axes for toolmanager interaction."""

    description = 'Enable all axes toolmanager'
    default_keymap = mpl.rcParams['keymap.all_axes']

    def trigger(self, sender, event, data=None):
        mpl.backend_bases.key_press_handler(event, self.figure.canvas, None)
