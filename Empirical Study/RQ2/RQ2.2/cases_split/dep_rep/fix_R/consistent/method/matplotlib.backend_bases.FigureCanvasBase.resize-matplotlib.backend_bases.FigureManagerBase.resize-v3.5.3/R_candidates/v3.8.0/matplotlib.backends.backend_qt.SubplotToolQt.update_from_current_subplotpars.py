    def update_from_current_subplotpars(self):
        self._defaults = {spinbox: getattr(self._figure.subplotpars, name)
                          for name, spinbox in self._spinboxes.items()}
        self._reset()  # Set spinbox current values without triggering signals.
