    def _uniform_y(self, N):
        '''
        Return colorbar data coordinates for *N* uniformly
        spaced boundaries, plus ends if required.
        '''
        if self.extend == 'neither':
            y = np.linspace(0, 1, N)
        else:
            automin = automax = 1. / (N - 1.)
            extendlength = self._get_extension_lengths(self.extendfrac,
                                                       automin, automax,
                                                       default=0.05)
            if self.extend == 'both':
                y = np.zeros(N + 2, 'd')
                y[0] = 0. - extendlength[0]
                y[-1] = 1. + extendlength[1]
            elif self.extend == 'min':
                y = np.zeros(N + 1, 'd')
                y[0] = 0. - extendlength[0]
            else:
                y = np.zeros(N + 1, 'd')
                y[-1] = 1. + extendlength[1]
            y[self._inside] = np.linspace(0, 1, N)
        return y
