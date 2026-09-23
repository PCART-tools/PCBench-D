    def transform(self, X, y=None):
        # 1D Series -> 2D DataFrame
        if hasattr(X, "to_frame"):
            return X.to_frame()
        # 1D array -> 2D array
        if X.ndim == 1:
            return np.atleast_2d(X).T
        return X
