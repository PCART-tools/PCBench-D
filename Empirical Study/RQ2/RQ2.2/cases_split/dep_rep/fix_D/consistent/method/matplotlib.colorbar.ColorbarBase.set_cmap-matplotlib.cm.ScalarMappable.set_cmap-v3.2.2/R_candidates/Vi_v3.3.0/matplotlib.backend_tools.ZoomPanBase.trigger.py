    def trigger(self, sender, event, data=None):
        self.toolmanager.get_tool(_views_positions).add_figure(self.figure)
        ToolToggleBase.trigger(self, sender, event, data)
