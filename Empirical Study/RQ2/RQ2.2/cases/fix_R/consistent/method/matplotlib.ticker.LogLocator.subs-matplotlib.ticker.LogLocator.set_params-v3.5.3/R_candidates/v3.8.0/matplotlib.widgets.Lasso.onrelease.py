    def onrelease(self, event):
        if self.ignore(event):
            return
        if self.verts is not None:
            self.verts.append(self._get_data_coords(event))
            if len(self.verts) > 2:
                self.callback(self.verts)
            self.line.remove()
        self.verts = None
        self.disconnect_events()
