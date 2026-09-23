    def set_mouseover(self, mouseover):
        """
        Set whether this artist is queried for custom context information when
        the mouse cursor moves over it.

        Parameters
        ----------
        mouseover : bool

        See Also
        --------
        get_cursor_data
        .ToolCursorPosition
        .NavigationToolbar2
        """
        self._mouseover = bool(mouseover)
        ax = self.axes
        if ax:
            if self._mouseover:
                ax._mouseover_set.add(self)
            else:
                ax._mouseover_set.discard(self)
