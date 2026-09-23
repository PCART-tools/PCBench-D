    def cla(self):
        super(ThetaAxis, self).cla()
        self.set_ticks_position('none')
        self._wrap_locator_formatter()
