    def _event_mpl_coords(self, event):
        # calling canvasx/canvasy allows taking scrollbars into account (i.e.
        # the top of the widget may have been scrolled out of view).
        return (self._tkcanvas.canvasx(event.x),
                # flipy so y=0 is bottom of canvas
                self.figure.bbox.height - self._tkcanvas.canvasy(event.y))
