    def _outline(self, X, Y):
        '''
        Return *x*, *y* arrays of colorbar bounding polygon,
        taking orientation into account.
        '''
        N = X.shape[0]
        ii = [0, 1, N - 2, N - 1, 2 * N - 1, 2 * N - 2, N + 1, N, 0]
        x = np.take(np.ravel(np.transpose(X)), ii)
        y = np.take(np.ravel(np.transpose(Y)), ii)
        x = x.reshape((len(x), 1))
        y = y.reshape((len(y), 1))
        if self.orientation == 'horizontal':
            return np.hstack((y, x))
        return np.hstack((x, y))
