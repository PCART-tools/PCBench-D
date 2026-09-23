    def remove_toolitem(self, name):
        for tool, handler in self._toolitems.pop(name, []):
            self.DeleteTool(tool.Id)
