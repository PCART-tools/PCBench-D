    def __init__(self, *args, **kwargs):
        StatusbarBase.__init__(self, *args, **kwargs)
        Gtk.Statusbar.__init__(self)
        self._context = self.get_context_id('message')
