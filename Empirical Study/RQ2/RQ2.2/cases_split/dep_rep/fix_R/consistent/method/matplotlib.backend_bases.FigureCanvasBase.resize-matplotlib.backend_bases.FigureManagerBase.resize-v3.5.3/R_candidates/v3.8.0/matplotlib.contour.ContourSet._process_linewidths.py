    def _process_linewidths(self, linewidths):
        Nlev = len(self.levels)
        if linewidths is None:
            default_linewidth = mpl.rcParams['contour.linewidth']
            if default_linewidth is None:
                default_linewidth = mpl.rcParams['lines.linewidth']
            return [default_linewidth] * Nlev
        elif not np.iterable(linewidths):
            return [linewidths] * Nlev
        else:
            linewidths = list(linewidths)
            return (linewidths * math.ceil(Nlev / len(linewidths)))[:Nlev]
