    @staticmethod
    def _get_uniform_grid_state(ticks):
        """
        Check whether all grid lines are in the same visibility state.

        Returns True/False if all grid lines are on or off, None if they are
        not all in the same state.
        """
        if all(tick.gridline.get_visible() for tick in ticks):
            return True
        elif not any(tick.gridline.get_visible() for tick in ticks):
            return False
        else:
            return None
