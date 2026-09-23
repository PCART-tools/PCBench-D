    def _process_linewidths(self):
        linewidths = self.linewidths
        Nlev = len(self.levels)
        if linewidths is None:
            tlinewidths = [(mpl.rcParams['lines.linewidth'],)] * Nlev
        else:
            if not np.iterable(linewidths):
                linewidths = [linewidths] * Nlev
            else:
                linewidths = list(linewidths)
                if len(linewidths) < Nlev:
                    nreps = int(np.ceil(Nlev / len(linewidths)))
                    linewidths = linewidths * nreps
                if len(linewidths) > Nlev:
                    linewidths = linewidths[:Nlev]
            tlinewidths = [(w,) for w in linewidths]
        return tlinewidths
