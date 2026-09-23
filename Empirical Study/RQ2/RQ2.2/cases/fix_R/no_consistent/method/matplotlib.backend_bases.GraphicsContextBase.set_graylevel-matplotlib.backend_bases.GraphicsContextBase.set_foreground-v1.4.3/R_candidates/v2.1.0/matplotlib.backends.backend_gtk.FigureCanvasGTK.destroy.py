    def destroy(self):
        #gtk.DrawingArea.destroy(self)
        self.close_event()
        if self._idle_draw_id != 0:
            gobject.source_remove(self._idle_draw_id)
