    def toggle_toolitem(self, name, toggled):
        if name not in self._toolitems:
            return
        for tool, handler in self._toolitems[name]:
            if not tool.IsControl():
                self.ToggleTool(tool.Id, toggled)
            else:
                tool.GetControl().SetValue(toggled)
        self.Refresh()
