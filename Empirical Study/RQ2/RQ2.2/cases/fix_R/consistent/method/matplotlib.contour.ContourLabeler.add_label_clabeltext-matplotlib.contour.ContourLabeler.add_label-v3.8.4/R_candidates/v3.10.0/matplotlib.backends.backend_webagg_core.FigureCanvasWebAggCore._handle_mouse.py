    def _handle_mouse(self, event):
        x = event['x']
        y = event['y']
        y = self.get_renderer().height - y
        self._last_mouse_xy = x, y
        e_type = event['type']
        button = event['button'] + 1  # JS numbers off by 1 compared to mpl.
        buttons = {  # JS ordering different compared to mpl.
            button for button, mask in [
                (MouseButton.LEFT, 1),
                (MouseButton.RIGHT, 2),
                (MouseButton.MIDDLE, 4),
                (MouseButton.BACK, 8),
                (MouseButton.FORWARD, 16),
            ] if event['buttons'] & mask  # State *after* press/release.
        }
        modifiers = event['modifiers']
        guiEvent = event.get('guiEvent')
        if e_type in ['button_press', 'button_release']:
            MouseEvent(e_type + '_event', self, x, y, button,
                       modifiers=modifiers, guiEvent=guiEvent)._process()
        elif e_type == 'dblclick':
            MouseEvent('button_press_event', self, x, y, button, dblclick=True,
                       modifiers=modifiers, guiEvent=guiEvent)._process()
        elif e_type == 'scroll':
            MouseEvent('scroll_event', self, x, y, step=event['step'],
                       modifiers=modifiers, guiEvent=guiEvent)._process()
        elif e_type == 'motion_notify':
            MouseEvent(e_type + '_event', self, x, y,
                       buttons=buttons, modifiers=modifiers, guiEvent=guiEvent,
                       )._process()
        elif e_type in ['figure_enter', 'figure_leave']:
            LocationEvent(e_type + '_event', self, x, y,
                          modifiers=modifiers, guiEvent=guiEvent)._process()
