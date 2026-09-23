    def set_theta_direction(self, direction):
        """
        Set the direction in which theta increases.

        clockwise, -1:
           Theta increases in the clockwise direction

        counterclockwise, anticlockwise, 1:
           Theta increases in the counterclockwise direction
        """
        mtx = self._direction.get_matrix()
        if direction in ('clockwise',):
            mtx[0, 0] = -1
        elif direction in ('counterclockwise', 'anticlockwise'):
            mtx[0, 0] = 1
        elif direction in (1, -1):
            mtx[0, 0] = direction
        else:
            raise ValueError(
                "direction must be 1, -1, clockwise or counterclockwise")
        self._direction.invalidate()
