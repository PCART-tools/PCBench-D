    def trigger(self, sender, event, data=None):
        ax = event.inaxes
        if ax is None:
            return
        try:
            x_state, x_which, y_state, y_which = self._get_next_grid_states(ax)
        except ValueError:
            pass
        else:
            ax.grid(x_state, which=x_which, axis="x")
            ax.grid(y_state, which=y_which, axis="y")
            ax.figure.canvas.draw_idle()
