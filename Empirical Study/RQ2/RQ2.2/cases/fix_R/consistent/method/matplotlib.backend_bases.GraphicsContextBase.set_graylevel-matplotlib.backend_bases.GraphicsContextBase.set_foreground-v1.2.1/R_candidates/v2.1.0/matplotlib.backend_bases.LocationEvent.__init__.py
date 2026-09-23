    def __init__(self, name, canvas, x, y, guiEvent=None):
        """
        *x*, *y* in figure coords, 0,0 = bottom, left
        """
        Event.__init__(self, name, canvas, guiEvent=guiEvent)
        self.x = x
        self.y = y

        if x is None or y is None:
            # cannot check if event was in axes if no x,y info
            self.inaxes = None
            self._update_enter_leave()
            return

        # Find all axes containing the mouse
        if self.canvas.mouse_grabber is None:
            axes_list = [a for a in self.canvas.figure.get_axes()
                         if a.in_axes(self)]
        else:
            axes_list = [self.canvas.mouse_grabber]

        if axes_list:  # Use highest zorder.
            self.inaxes = max(axes_list, key=lambda x: x.zorder)
        else:  # None found.
            self.inaxes = None
            self._update_enter_leave()
            return

        try:
            trans = self.inaxes.transData.inverted()
            xdata, ydata = trans.transform_point((x, y))
        except ValueError:
            self.xdata = None
            self.ydata = None
        else:
            self.xdata = xdata
            self.ydata = ydata

        self._update_enter_leave()
