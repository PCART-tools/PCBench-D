    def _get_next_grid_states(self, ax):
        if None in map(self._get_uniform_grid_state,
                       [ax.xaxis.minorTicks, ax.yaxis.minorTicks]):
            # Bail out if minor grids are not in a uniform state.
            raise ValueError
        x_state, y_state = map(self._get_uniform_grid_state,
                               [ax.xaxis.majorTicks, ax.yaxis.majorTicks])
        cycle = self._cycle
        # Bail out (via ValueError) if major grids are not in a uniform state.
        x_state, y_state = (
            cycle[(cycle.index((x_state, y_state)) + 1) % len(cycle)])
        return (x_state, "major" if x_state else "both",
                y_state, "major" if y_state else "both")
