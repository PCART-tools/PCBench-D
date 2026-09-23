    def remove_toolitem(self, name):
        for toolitem in self._toolitems[name]:
            toolitem.pack_forget()
        del self._toolitems[name]
