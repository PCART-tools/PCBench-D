    def new_frame_seq(self):
        '''Creates a new sequence of frame information.'''
        # Default implementation is just an iterator over self._framedata
        return iter(self._framedata)
