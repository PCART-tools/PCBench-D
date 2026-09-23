    def remove_toolitem(self, name):
        for button, handler in self._toolitems[name]:
            button.setParent(None)
        del self._toolitems[name]
