    def _reset(self):
        for attr, value in self._defaults.items():
            self._widgets[attr].setValue(value)
