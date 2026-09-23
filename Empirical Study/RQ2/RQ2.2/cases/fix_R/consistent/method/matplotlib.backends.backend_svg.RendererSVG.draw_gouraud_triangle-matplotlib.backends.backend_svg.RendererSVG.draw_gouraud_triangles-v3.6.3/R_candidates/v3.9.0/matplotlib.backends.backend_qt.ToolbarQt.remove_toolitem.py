    def remove_toolitem(self, name):
        for button, handler in self._toolitems.pop(name, []):
            button.setParent(None)
