    def __init__(self, ax, x, y, marker='o', marker_props=None, useblit=True):
        self.ax = ax
        props = dict(marker=marker, markersize=7, mfc='w', ls='none',
                     alpha=0.5, visible=False, label='_nolegend_')
        props.update(marker_props if marker_props is not None else {})
        self._markers = Line2D(x, y, animated=useblit, **props)
        self.ax.add_line(self._markers)
        self.artist = self._markers
