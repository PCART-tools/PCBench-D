    def __init__(self, ax, x, y, marker='o', marker_props=None, useblit=True):
        self.ax = ax
        props = {'marker': marker, 'markersize': 7, 'markerfacecolor': 'w',
                 'linestyle': 'none', 'alpha': 0.5, 'visible': False,
                 'label': '_nolegend_',
                 **cbook.normalize_kwargs(marker_props, Line2D._alias_map)}
        self._markers = Line2D(x, y, animated=useblit, **props)
        self.ax.add_line(self._markers)
