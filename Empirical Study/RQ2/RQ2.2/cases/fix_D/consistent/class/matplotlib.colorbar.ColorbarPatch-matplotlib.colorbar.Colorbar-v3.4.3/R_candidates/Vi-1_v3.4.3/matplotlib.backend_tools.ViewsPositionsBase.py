class ViewsPositionsBase(ToolBase):
    """Base class for `ToolHome`, `ToolBack` and `ToolForward`."""

    _on_trigger = None

    def trigger(self, sender, event, data=None):
        self.toolmanager.get_tool(_views_positions).add_figure(self.figure)
        getattr(self.toolmanager.get_tool(_views_positions),
                self._on_trigger)()
        self.toolmanager.get_tool(_views_positions).update_view()
