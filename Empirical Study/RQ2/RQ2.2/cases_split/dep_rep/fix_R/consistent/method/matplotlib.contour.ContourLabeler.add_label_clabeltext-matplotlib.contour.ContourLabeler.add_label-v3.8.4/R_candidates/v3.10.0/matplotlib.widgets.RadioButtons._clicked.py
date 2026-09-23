    def _clicked(self, event):
        if self.ignore(event) or event.button != 1 or not self.ax.contains(event)[0]:
            return
        idxs = [  # Indices of buttons and of texts that contain the event.
            *self._buttons.contains(event)[1]["ind"],
            *[i for i, text in enumerate(self.labels) if text.contains(event)[0]]]
        if idxs:
            coords = self._buttons.get_offset_transform().transform(
                self._buttons.get_offsets())
            self.set_active(  # Closest index, only looking in idxs.
                idxs[(((event.x, event.y) - coords[idxs]) ** 2).sum(-1).argmin()])
