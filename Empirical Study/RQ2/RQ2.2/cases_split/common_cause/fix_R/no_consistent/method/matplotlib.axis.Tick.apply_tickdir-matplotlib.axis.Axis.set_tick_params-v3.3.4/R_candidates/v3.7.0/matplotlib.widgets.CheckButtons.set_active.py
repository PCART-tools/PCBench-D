    def set_active(self, index):
        """
        Toggle (activate or deactivate) a check button by index.

        Callbacks will be triggered if :attr:`eventson` is True.

        Parameters
        ----------
        index : int
            Index of the check button to toggle.

        Raises
        ------
        ValueError
            If *index* is invalid.
        """
        if index not in range(len(self.labels)):
            raise ValueError(f'Invalid CheckButton index: {index}')

        invisible = colors.to_rgba('none')

        facecolors = self._checks.get_facecolor()
        facecolors[index] = (
            self._active_check_colors[index]
            if colors.same_color(facecolors[index], invisible)
            else invisible
        )
        self._checks.set_facecolor(facecolors)

        if hasattr(self, "_lines"):
            l1, l2 = self._lines[index]
            l1.set_visible(not l1.get_visible())
            l2.set_visible(not l2.get_visible())

        if self.drawon:
            if self._useblit:
                if self._background is not None:
                    self.canvas.restore_region(self._background)
                self.ax.draw_artist(self._checks)
                if hasattr(self, "_lines"):
                    for l1, l2 in self._lines:
                        self.ax.draw_artist(l1)
                        self.ax.draw_artist(l2)
                self.canvas.blit(self.ax.bbox)
            else:
                self.canvas.draw()

        if self.eventson:
            self._observers.process('clicked', self.labels[index].get_text())
