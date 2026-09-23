    def _edges(self, X, Y):
        '''
        Return the separator line segments; helper for _add_solids.
        '''
        N = X.shape[0]
        # Using the non-array form of these line segments is much
        # simpler than making them into arrays.
        if self.orientation == 'vertical':
            return [list(zip(X[i], Y[i])) for i in xrange(1, N - 1)]
        else:
            return [list(zip(Y[i], X[i])) for i in xrange(1, N - 1)]
