    def button_press_event(self, event, dblclick=False):
        # set focus to the canvas so that it can receive keyboard events
        self._tkcanvas.focus_set()

        num = getattr(event, 'num', None)
        if sys.platform == 'darwin':  # 2 and 3 are reversed.
            num = {2: 3, 3: 2}.get(num, num)
        MouseEvent("button_press_event", self,
                   *self._event_mpl_coords(event), num, dblclick=dblclick,
                   modifiers=self._mpl_modifiers(event),
                   guiEvent=event)._process()
