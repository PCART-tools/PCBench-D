    def draggable(self, state=None, use_blit=False, update="loc"):
        """
        Set the draggable state -- if state is

          * None : toggle the current state

          * True : turn draggable on

          * False : turn draggable off

        If draggable is on, you can drag the legend on the canvas with
        the mouse. The `.DraggableLegend` helper instance is returned if
        draggable is on.

        The update parameter control which parameter of the legend changes
        when dragged. If update is "loc", the *loc* parameter of the legend
        is changed. If "bbox", the *bbox_to_anchor* parameter is changed.
        """
        warn_deprecated("2.2",
                        message="Legend.draggable() is drepecated in "
                                "favor of Legend.set_draggable(). "
                                "Legend.draggable may be reintroduced as a "
                                "property in future releases.")

        if state is None:
            state = not self.get_draggable()  # toggle state

        self.set_draggable(state, use_blit, update)

        return self._draggable
