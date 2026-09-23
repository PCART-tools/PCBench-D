    def _process_linestyles(self):
        linestyles = self.linestyles
        Nlev = len(self.levels)
        if linestyles is None:
            tlinestyles = ['solid'] * Nlev
            if self.monochrome:
                neg_ls = mpl.rcParams['contour.negative_linestyle']
                eps = - (self.zmax - self.zmin) * 1e-15
                for i, lev in enumerate(self.levels):
                    if lev < eps:
                        tlinestyles[i] = neg_ls
        else:
            if isinstance(linestyles, six.string_types):
                tlinestyles = [linestyles] * Nlev
            elif cbook.iterable(linestyles):
                tlinestyles = list(linestyles)
                if len(tlinestyles) < Nlev:
                    nreps = int(np.ceil(Nlev / len(linestyles)))
                    tlinestyles = tlinestyles * nreps
                if len(tlinestyles) > Nlev:
                    tlinestyles = tlinestyles[:Nlev]
            else:
                raise ValueError("Unrecognized type for linestyles kwarg")
        return tlinestyles
