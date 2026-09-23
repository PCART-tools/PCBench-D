    def flush_events(self):
        gtk.gdk.threads_enter()
        while gtk.events_pending():
            gtk.main_iteration(True)
        gtk.gdk.flush()
        gtk.gdk.threads_leave()
