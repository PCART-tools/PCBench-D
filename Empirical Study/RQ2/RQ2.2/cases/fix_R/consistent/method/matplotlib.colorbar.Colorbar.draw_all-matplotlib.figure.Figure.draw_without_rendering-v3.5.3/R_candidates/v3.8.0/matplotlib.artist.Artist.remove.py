    def remove(self):
        """
        Remove the artist from the figure if possible.

        The effect will not be visible until the figure is redrawn, e.g.,
        with `.FigureCanvasBase.draw_idle`.  Call `~.axes.Axes.relim` to
        update the axes limits if desired.

        Note: `~.axes.Axes.relim` will not see collections even if the
        collection was added to the axes with *autolim* = True.

        Note: there is no support for removing the artist's legend entry.
        """

        # There is no method to set the callback.  Instead, the parent should
        # set the _remove_method attribute directly.  This would be a
        # protected attribute if Python supported that sort of thing.  The
        # callback has one parameter, which is the child to be removed.
        if self._remove_method is not None:
            self._remove_method(self)
            # clear stale callback
            self.stale_callback = None
            _ax_flag = False
            if hasattr(self, 'axes') and self.axes:
                # remove from the mouse hit list
                self.axes._mouseover_set.discard(self)
                self.axes.stale = True
                self.axes = None  # decouple the artist from the Axes
                _ax_flag = True

            if self.figure:
                if not _ax_flag:
                    self.figure.stale = True
                self.figure = None

        else:
            raise NotImplementedError('cannot remove artist')
