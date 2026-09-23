    def clear(self):
        super().clear()
        self.set_ticks_position('none')
        self._wrap_locator_formatter()
