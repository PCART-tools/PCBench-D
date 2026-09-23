    def destroy(self):
        #Gtk.DrawingArea.destroy(self)
        self.close_event()
        if self._idle_draw_id != 0:
            GLib.source_remove(self._idle_draw_id)
