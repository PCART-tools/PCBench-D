    def set_active(self, index, state=None):
        """
        Modify the state of a check button by index.

        Callbacks will be triggered if :attr:`eventson` is True.

        Parameters
        ----------
        index : int
            Index of the check button to toggle.

        state : bool, optional
            If a boolean value, set the state explicitly. If no value is
            provided, the state is toggled.

        Raises
        ------
        ValueError
            If *index* is invalid.
        TypeError
            If *state* is not boolean.
        """
        if index not in range(len(self.labels)):
            raise ValueError(f'Invalid CheckButton index: {index}')
        _api.check_isinstance((bool, None), state=state)

        invisible = colors.to_rgba('none')

        facecolors = self._checks.get_facecolor()
        if state is None:
            state = colors.same_color(facecolors[index], invisible)
        facecolors[index] = self._active_check_colors[index] if state else invisible
        self._checks.set_facecolor(facecolors)

        if self.drawon:
            if self._useblit:
                if self._background is not None:
                    self.canvas.restore_region(self._background)
                self.ax.draw_artist(self._checks)
                self.canvas.blit(self.ax.bbox)
            else:
                self.canvas.draw()

        if self.eventson:
            self._observers.process('clicked', self.labels[index].get_text())
