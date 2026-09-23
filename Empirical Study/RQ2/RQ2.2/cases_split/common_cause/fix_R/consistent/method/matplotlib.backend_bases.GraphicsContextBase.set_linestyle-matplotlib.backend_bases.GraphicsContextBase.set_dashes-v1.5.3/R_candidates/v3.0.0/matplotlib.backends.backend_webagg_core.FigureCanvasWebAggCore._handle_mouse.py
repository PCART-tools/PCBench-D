    def _handle_mouse(self, event):
        x = event['x']
        y = event['y']
        y = self.get_renderer().height - y

        # Javascript button numbers and matplotlib button numbers are
        # off by 1
        button = event['button'] + 1

        # The right mouse button pops up a context menu, which
        # doesn't work very well, so use the middle mouse button
        # instead.  It doesn't seem that it's possible to disable
        # the context menu in recent versions of Chrome.  If this
        # is resolved, please also adjust the docstring in MouseEvent.
        if button == 2:
            button = 3

        e_type = event['type']
        guiEvent = event.get('guiEvent', None)
        if e_type == 'button_press':
            self.button_press_event(x, y, button, guiEvent=guiEvent)
        elif e_type == 'button_release':
            self.button_release_event(x, y, button, guiEvent=guiEvent)
        elif e_type == 'motion_notify':
            self.motion_notify_event(x, y, guiEvent=guiEvent)
        elif e_type == 'figure_enter':
            self.enter_notify_event(xy=(x, y), guiEvent=guiEvent)
        elif e_type == 'figure_leave':
            self.leave_notify_event()
        elif e_type == 'scroll':
            self.scroll_event(x, y, event['step'], guiEvent=guiEvent)
