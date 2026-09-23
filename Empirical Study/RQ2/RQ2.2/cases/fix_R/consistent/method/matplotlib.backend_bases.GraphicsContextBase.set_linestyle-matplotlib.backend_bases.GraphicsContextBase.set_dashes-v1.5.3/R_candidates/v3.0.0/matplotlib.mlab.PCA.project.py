    def project(self, x, minfrac=0.):
        '''
        project x onto the principle axes, dropping any axes where fraction
        of variance<minfrac
        '''
        x = np.asarray(x)
        if x.shape[-1] != self.numcols:
            raise ValueError('Expected an array with dims[-1]==%d' %
                             self.numcols)
        Y = np.dot(self.Wt, self.center(x).T).T
        mask = self.fracs >= minfrac
        if x.ndim == 2:
            Yreduced = Y[:, mask]
        else:
            Yreduced = Y[mask]
        return Yreduced
