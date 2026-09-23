    def remove_toolitem(self, name):
        for toolitem in self._toolitems.pop(name, []):
            toolitem.pack_forget()
