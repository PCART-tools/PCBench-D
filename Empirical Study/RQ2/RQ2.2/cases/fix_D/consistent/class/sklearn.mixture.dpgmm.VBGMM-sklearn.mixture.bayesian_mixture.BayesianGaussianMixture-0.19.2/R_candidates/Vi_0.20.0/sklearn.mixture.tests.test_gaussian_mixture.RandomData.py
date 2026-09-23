class RandomData(object):
    def __init__(self, rng, n_samples=500, n_components=2, n_features=2,
                 scale=50):
        self.n_samples = n_samples
        self.n_components = n_components
        self.n_features = n_features

        self.weights = rng.rand(n_components)
        self.weights = self.weights / self.weights.sum()
        self.means = rng.rand(n_components, n_features) * scale
        self.covariances = {
            'spherical': .5 + rng.rand(n_components),
            'diag': (.5 + rng.rand(n_components, n_features)) ** 2,
            'tied': make_spd_matrix(n_features, random_state=rng),
            'full': np.array([
                make_spd_matrix(n_features, random_state=rng) * .5
                for _ in range(n_components)])}
        self.precisions = {
            'spherical': 1. / self.covariances['spherical'],
            'diag': 1. / self.covariances['diag'],
            'tied': linalg.inv(self.covariances['tied']),
            'full': np.array([linalg.inv(covariance)
                             for covariance in self.covariances['full']])}

        self.X = dict(zip(COVARIANCE_TYPE, [generate_data(
            n_samples, n_features, self.weights, self.means, self.covariances,
            covar_type) for covar_type in COVARIANCE_TYPE]))
        self.Y = np.hstack([np.full(int(np.round(w * n_samples)), k,
                                    dtype=np.int)
                            for k, w in enumerate(self.weights)])
