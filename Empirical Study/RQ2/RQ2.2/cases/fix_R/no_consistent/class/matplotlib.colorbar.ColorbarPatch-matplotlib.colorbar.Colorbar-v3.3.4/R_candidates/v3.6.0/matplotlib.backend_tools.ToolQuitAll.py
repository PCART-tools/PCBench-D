class ToolQuitAll(ToolBase):
    """Tool to call the figure manager destroy method."""

    description = 'Quit all figures'
    default_keymap = property(lambda self: mpl.rcParams['keymap.quit_all'])

    def trigger(self, sender, event, data=None):
        Gcf.destroy_all()
