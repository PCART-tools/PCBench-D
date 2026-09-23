    def calc_window_target(self, x, NFFT, noverlap=0, axis=0):
        '''This is an adaptation of the original window extraction
        algorithm.  This is here to test to make sure the new implementation
        has the same result'''
        step = NFFT - noverlap
        ind = np.arange(0, len(x) - NFFT + 1, step)
        n = len(ind)
        result = np.zeros((NFFT, n))

        # do the ffts of the slices
        for i in range(n):
            result[:, i] = x[ind[i]:ind[i]+NFFT]
        if axis == 1:
            result = result.T
        return result
