    def _bounds_from_inset_ax(self):
        xlim = self._inset_ax.get_xlim()
        ylim = self._inset_ax.get_ylim()
        return (xlim[0], ylim[0], xlim[1] - xlim[0], ylim[1] - ylim[0])
