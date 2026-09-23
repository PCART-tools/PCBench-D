    def get_positions(self):
        '''
        return an array containing the floating-point values of the positions
        '''
        segments = self.get_segments()
        pos = 0 if self.is_horizontal() else 1
        positions = []
        for segment in segments:
            positions.append(segment[0, pos])
        return positions
