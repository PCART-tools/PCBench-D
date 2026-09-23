    def remove_toolitem(self, name):
        if name not in self._toolitems:
            self.toolmanager.message_event(f'{name} not in toolbar', self)
            return

        for group in self._groups:
            for toolitem, _signal in self._toolitems[name]:
                if toolitem in self._groups[group]:
                    self._groups[group].remove(toolitem)
        del self._toolitems[name]
