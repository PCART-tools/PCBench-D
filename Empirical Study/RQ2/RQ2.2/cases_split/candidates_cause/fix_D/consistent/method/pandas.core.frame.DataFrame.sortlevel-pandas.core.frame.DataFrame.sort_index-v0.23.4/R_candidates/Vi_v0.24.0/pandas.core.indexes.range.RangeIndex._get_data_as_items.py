    def _get_data_as_items(self):
        """ return a list of tuples of start, stop, step """
        return [('start', self._start),
                ('stop', self._stop),
                ('step', self._step)]
