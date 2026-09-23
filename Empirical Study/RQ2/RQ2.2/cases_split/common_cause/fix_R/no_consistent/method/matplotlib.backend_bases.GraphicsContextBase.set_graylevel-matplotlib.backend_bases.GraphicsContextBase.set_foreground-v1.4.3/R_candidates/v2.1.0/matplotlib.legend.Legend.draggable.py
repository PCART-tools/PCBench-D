    def draggable(self, state=None, use_blit=False, update="loc"):
        """
        Set the draggable state -- if state is

          * None : toggle the current state

          * True : turn draggable on

          * False : turn draggable off

        If draggable is on, you can drag the legend on the canvas with
        the mouse.  The DraggableLegend helper instance is returned if
        draggable is on.

        The update parameter control which parameter of the legend changes
        when dragged. If update is "loc", the *loc* parameter of the legend
        is changed. If "bbox", the *bbox_to_anchor* parameter is changed.
        """
        is_draggable = self._draggable is not None

        # if state is None we'll toggle
        if state is None:
            state = not is_draggable

        if state:
            if self._draggable is None:
                self._draggable = DraggableLegend(self,
                                                  use_blit,
                                                  update=update)
        else:
            if self._draggable is not None:
                self._draggable.disconnect()
            self._draggable = None

        return self._draggable
