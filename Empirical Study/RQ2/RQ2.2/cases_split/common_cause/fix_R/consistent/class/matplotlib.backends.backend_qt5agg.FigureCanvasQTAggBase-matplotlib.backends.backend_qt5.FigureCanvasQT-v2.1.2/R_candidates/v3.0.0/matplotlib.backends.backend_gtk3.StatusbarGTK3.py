class StatusbarGTK3(StatusbarBase, Gtk.Statusbar):
    def __init__(self, *args, **kwargs):
        StatusbarBase.__init__(self, *args, **kwargs)
        Gtk.Statusbar.__init__(self)
        self._context = self.get_context_id('message')

    def set_message(self, s):
        self.pop(self._context)
        self.push(self._context, s)
