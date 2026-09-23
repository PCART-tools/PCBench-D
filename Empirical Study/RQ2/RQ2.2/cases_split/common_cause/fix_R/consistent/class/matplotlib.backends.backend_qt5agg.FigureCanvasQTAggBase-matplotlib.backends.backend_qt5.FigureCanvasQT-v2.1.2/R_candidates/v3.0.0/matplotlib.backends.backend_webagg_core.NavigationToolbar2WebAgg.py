class NavigationToolbar2WebAgg(backend_bases.NavigationToolbar2):

    # Use the standard toolbar items + download button
    toolitems = [(text, tooltip_text, _JQUERY_ICON_CLASSES[image_file],
                  name_of_method)
                 for text, tooltip_text, image_file, name_of_method
                 in (backend_bases.NavigationToolbar2.toolitems +
                     (('Download', 'Download plot', 'download', 'download'),))
                 if image_file in _JQUERY_ICON_CLASSES]

    def _init_toolbar(self):
        self.message = ''
        self.cursor = 0

    def set_message(self, message):
        if message != self.message:
            self.canvas.send_event("message", message=message)
        self.message = message

    def set_cursor(self, cursor):
        if cursor != self.cursor:
            self.canvas.send_event("cursor", cursor=cursor)
        self.cursor = cursor

    def draw_rubberband(self, event, x0, y0, x1, y1):
        self.canvas.send_event(
            "rubberband", x0=x0, y0=y0, x1=x1, y1=y1)

    def release_zoom(self, event):
        backend_bases.NavigationToolbar2.release_zoom(self, event)
        self.canvas.send_event(
            "rubberband", x0=-1, y0=-1, x1=-1, y1=-1)

    def save_figure(self, *args):
        """Save the current figure"""
        self.canvas.send_event('save')
