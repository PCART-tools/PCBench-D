    def _outline(self, X, Y):
        """
        Return *x*, *y* arrays of colorbar bounding polygon,
        taking orientation into account.
        """
        N = X.shape[0]
        ii = [0, 1, N - 2, N - 1, 2 * N - 1, 2 * N - 2, N + 1, N, 0]
        x = X.T.reshape(-1)[ii]
        y = Y.T.reshape(-1)[ii]
        return (np.column_stack([y, x])
                if self.orientation == 'horizontal' else
                np.column_stack([x, y]))
