    def scroll_event(self, controller, dx, dy):
        MouseEvent("scroll_event", self,
                   *self._mpl_coords(), step=dy)._process()
        return True
