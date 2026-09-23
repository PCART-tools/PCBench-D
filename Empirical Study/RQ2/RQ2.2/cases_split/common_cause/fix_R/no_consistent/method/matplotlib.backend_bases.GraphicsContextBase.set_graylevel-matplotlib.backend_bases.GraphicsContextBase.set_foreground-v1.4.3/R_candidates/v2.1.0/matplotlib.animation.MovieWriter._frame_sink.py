    def _frame_sink(self):
        '''Returns the place to which frames should be written.'''
        return self._proc.stdin
