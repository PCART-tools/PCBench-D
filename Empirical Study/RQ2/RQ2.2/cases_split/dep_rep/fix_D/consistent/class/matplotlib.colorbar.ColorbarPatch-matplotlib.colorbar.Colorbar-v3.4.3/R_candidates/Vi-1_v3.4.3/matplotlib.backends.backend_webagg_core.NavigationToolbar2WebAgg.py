class NavigationToolbar2WebAgg(backend_bases.NavigationToolbar2):

    # Use the standard toolbar items + download button
    toolitems = [
        (text, tooltip_text, image_file, name_of_method)
        for text, tooltip_text, image_file, name_of_method
        in (*backend_bases.NavigationToolbar2.toolitems,
            ('Download', 'Download plot', 'filesave', 'download'))
        if name_of_method in _ALLOWED_TOOL_ITEMS
    ]

    def __init__(self, canvas):
        self.message = ''
        self.cursor = 0
        super().__init__(canvas)

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
        super().release_zoom(event)
        self.canvas.send_event(
            "rubberband", x0=-1, y0=-1, x1=-1, y1=-1)

    def save_figure(self, *args):
        """Save the current figure"""
        self.canvas.send_event('save')

    def pan(self):
        super().pan()
        self.canvas.send_event('navigate_mode', mode=self.mode.name)

    def zoom(self):
        super().zoom()
        self.canvas.send_event('navigate_mode', mode=self.mode.name)

    def set_history_buttons(self):
        can_backward = self._nav_stack._pos > 0
        can_forward = self._nav_stack._pos < len(self._nav_stack._elements) - 1
        self.canvas.send_event('history_buttons',
                               Back=can_backward, Forward=can_forward)
