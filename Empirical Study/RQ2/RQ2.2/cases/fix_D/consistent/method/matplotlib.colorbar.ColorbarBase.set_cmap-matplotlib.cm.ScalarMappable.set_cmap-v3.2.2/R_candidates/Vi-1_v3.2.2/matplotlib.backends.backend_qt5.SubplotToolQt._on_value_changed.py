    def _on_value_changed(self):
        self._figure.subplots_adjust(**{attr: self._widgets[attr].value()
                                        for attr in self._attrs})
        self._figure.canvas.draw_idle()
