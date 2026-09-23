    def flush_events(self):
        # docstring inherited
        Gdk.threads_enter()
        while Gtk.events_pending():
            Gtk.main_iteration()
        Gdk.flush()
        Gdk.threads_leave()
