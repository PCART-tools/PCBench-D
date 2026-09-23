    def check_window_apply_repeat(self, x, window, NFFT, noverlap):
        '''This is an adaptation of the original window application
        algorithm.  This is here to test to make sure the new implementation
        has the same result'''
        step = NFFT - noverlap
        ind = np.arange(0, len(x) - NFFT + 1, step)
        n = len(ind)
        result = np.zeros((NFFT, n))

        if cbook.iterable(window):
            windowVals = window
        else:
            windowVals = window(np.ones((NFFT,), x.dtype))

        # do the ffts of the slices
        for i in range(n):
            result[:, i] = windowVals * x[ind[i]:ind[i]+NFFT]
        return result
