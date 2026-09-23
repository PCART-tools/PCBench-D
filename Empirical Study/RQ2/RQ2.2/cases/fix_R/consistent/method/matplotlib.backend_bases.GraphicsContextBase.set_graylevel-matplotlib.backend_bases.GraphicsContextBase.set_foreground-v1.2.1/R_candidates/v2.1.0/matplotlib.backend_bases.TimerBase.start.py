    def start(self, interval=None):
        '''
        Start the timer object. `interval` is optional and will be used
        to reset the timer interval first if provided.
        '''
        if interval is not None:
            self._set_interval(interval)
        self._timer_start()
