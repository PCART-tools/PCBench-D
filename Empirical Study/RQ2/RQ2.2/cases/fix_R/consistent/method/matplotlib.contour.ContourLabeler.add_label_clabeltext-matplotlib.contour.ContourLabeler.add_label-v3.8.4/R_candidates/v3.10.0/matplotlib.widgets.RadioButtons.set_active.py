    def set_active(self, index):
        """
        Select button with number *index*.

        Callbacks will be triggered if :attr:`eventson` is True.

        Parameters
        ----------
        index : int
            The index of the button to activate.

        Raises
        ------
        ValueError
            If the index is invalid.
        """
        if index not in range(len(self.labels)):
            raise ValueError(f'Invalid RadioButton index: {index}')
        self.value_selected = self.labels[index].get_text()
        self.index_selected = index
        button_facecolors = self._buttons.get_facecolor()
        button_facecolors[:] = colors.to_rgba("none")
        button_facecolors[index] = colors.to_rgba(self._active_colors[index])
        self._buttons.set_facecolor(button_facecolors)

        if self.drawon:
            if self._useblit:
                if self._background is not None:
                    self.canvas.restore_region(self._background)
                self.ax.draw_artist(self._buttons)
                self.canvas.blit(self.ax.bbox)
            else:
                self.canvas.draw()

        if self.eventson:
            self._observers.process('clicked', self.labels[index].get_text())
