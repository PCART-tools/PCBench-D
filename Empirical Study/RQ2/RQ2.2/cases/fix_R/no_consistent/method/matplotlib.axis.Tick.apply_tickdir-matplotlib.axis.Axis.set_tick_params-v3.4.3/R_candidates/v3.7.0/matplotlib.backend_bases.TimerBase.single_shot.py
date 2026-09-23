    @single_shot.setter
    def single_shot(self, ss):
        self._single = ss
        self._timer_set_single_shot()
