    def remove_toolitem(self, name):
        for tool, handler in self._toolitems[name]:
            self.DeleteTool(tool.Id)
        del self._toolitems[name]
