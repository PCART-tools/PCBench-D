    def set_positions(self, positions):
        '''
        set the positions of the events to the specified value
        '''
        if positions is None or (hasattr(positions, 'len') and
                                 len(positions) == 0):
            self.set_segments([])
            return

        lineoffset = self.get_lineoffset()
        linelength = self.get_linelength()
        segment = (lineoffset + linelength / 2.,
                   lineoffset - linelength / 2.)
        positions = np.asanyarray(positions)
        positions.sort()
        if self.is_horizontal():
            segments = [[(coord1, coord2) for coord2 in segment] for
                        coord1 in positions]
        else:
            segments = [[(coord2, coord1) for coord2 in segment] for
                        coord1 in positions]
        self.set_segments(segments)
