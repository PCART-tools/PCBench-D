    def scroll_event(self, event):
        num = getattr(event, 'num', None)
        step = 1 if num == 4 else -1 if num == 5 else 0
        MouseEvent("scroll_event", self,
                   *self._event_mpl_coords(event), step=step,
                   modifiers=self._mpl_modifiers(event),
                   guiEvent=event)._process()
