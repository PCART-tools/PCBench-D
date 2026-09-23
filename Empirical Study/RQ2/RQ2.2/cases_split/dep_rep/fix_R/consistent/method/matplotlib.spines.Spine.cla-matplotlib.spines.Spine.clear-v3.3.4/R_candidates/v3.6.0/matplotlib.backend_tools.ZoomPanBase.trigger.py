    def trigger(self, sender, event, data=None):
        self.toolmanager.get_tool(_views_positions).add_figure(self.figure)
        super().trigger(sender, event, data)
        new_navigate_mode = self.name.upper() if self.toggled else None
        for ax in self.figure.axes:
            ax.set_navigate_mode(new_navigate_mode)
