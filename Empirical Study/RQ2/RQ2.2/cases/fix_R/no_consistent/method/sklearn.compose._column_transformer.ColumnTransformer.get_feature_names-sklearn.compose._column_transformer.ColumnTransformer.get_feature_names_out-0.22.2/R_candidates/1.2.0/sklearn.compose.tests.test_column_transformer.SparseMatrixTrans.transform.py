    def transform(self, X, y=None):
        n_samples = len(X)
        return sparse.eye(n_samples, n_samples).tocsr()
