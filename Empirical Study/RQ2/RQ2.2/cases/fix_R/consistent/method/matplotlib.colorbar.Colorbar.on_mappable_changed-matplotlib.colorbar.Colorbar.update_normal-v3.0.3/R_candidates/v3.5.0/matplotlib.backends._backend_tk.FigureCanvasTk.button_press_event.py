    def button_press_event(self, event, dblclick=False):
        num = getattr(event, 'num', None)
        if sys.platform == 'darwin':  # 2 and 3 are reversed.
            num = {2: 3, 3: 2}.get(num, num)
        super().button_press_event(
            *self._event_mpl_coords(event), num, dblclick=dblclick,
            guiEvent=event)
