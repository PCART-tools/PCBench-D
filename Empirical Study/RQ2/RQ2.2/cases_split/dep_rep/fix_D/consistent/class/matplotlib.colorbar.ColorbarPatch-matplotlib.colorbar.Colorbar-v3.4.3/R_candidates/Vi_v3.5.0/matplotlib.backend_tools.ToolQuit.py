class ToolQuit(ToolBase):
    """Tool to call the figure manager destroy method."""

    description = 'Quit the figure'
    default_keymap = mpl.rcParams['keymap.quit']

    def trigger(self, sender, event, data=None):
        Gcf.destroy_fig(self.figure)
