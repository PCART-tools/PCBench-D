    def _tight_layout(self):
        self._figure.tight_layout()
        for attr, spinbox in self._spinboxes.items():
            spinbox.blockSignals(True)
            spinbox.setValue(vars(self._figure.subplotpars)[attr])
            spinbox.blockSignals(False)
        self._figure.canvas.draw_idle()
