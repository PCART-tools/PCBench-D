    def switch_orientation(self):
        '''
        switch the orientation of the event line, either from vertical to
        horizontal or vice versus
        '''
        segments = self.get_segments()
        for i, segment in enumerate(segments):
            segments[i] = np.fliplr(segment)
        self.set_segments(segments)
        self._is_horizontal = not self.is_horizontal()
        self.stale = True
