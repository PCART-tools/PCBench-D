class GMMTester():
    do_test_eval = True

    def _setUp(self):
        self.n_components = 10
        self.n_features = 4
        self.weights = rng.rand(self.n_components)
        self.weights = self.weights / self.weights.sum()
        self.means = rng.randint(-20, 20, (self.n_components, self.n_features))
        self.threshold = -0.5
        self.I = np.eye(self.n_features)
        self.covars = {
            'spherical': (0.1 + 2 * rng.rand(self.n_components,
                                             self.n_features)) ** 2,
            'tied': (make_spd_matrix(self.n_features, random_state=0)
                     + 5 * self.I),
            'diag': (0.1 + 2 * rng.rand(self.n_components,
                                        self.n_features)) ** 2,
            'full': np.array([make_spd_matrix(self.n_features, random_state=0)
                              + 5 * self.I for x in range(self.n_components)])}

    # This function tests the deprecated old GMM class
    @ignore_warnings(category=DeprecationWarning)
    def test_eval(self):
        if not self.do_test_eval:
            return  # DPGMM does not support setting the means and
        # covariances before fitting There is no way of fixing this
        # due to the variational parameters being more expressive than
        # covariance matrices
        g = self.model(n_components=self.n_components,
                       covariance_type=self.covariance_type, random_state=rng)
        # Make sure the means are far apart so responsibilities.argmax()
        # picks the actual component used to generate the observations.
        g.means_ = 20 * self.means
        g.covars_ = self.covars[self.covariance_type]
        g.weights_ = self.weights

        gaussidx = np.repeat(np.arange(self.n_components), 5)
        n_samples = len(gaussidx)
        X = rng.randn(n_samples, self.n_features) + g.means_[gaussidx]

        with ignore_warnings(category=DeprecationWarning):
            ll, responsibilities = g.score_samples(X)

        self.assertEqual(len(ll), n_samples)
        self.assertEqual(responsibilities.shape,
                         (n_samples, self.n_components))
        assert_array_almost_equal(responsibilities.sum(axis=1),
                                  np.ones(n_samples))
        assert_array_equal(responsibilities.argmax(axis=1), gaussidx)

    # This function tests the deprecated old GMM class
    @ignore_warnings(category=DeprecationWarning)
    def test_sample(self, n=100):
        g = self.model(n_components=self.n_components,
                       covariance_type=self.covariance_type,
                       random_state=rng)
        # Make sure the means are far apart so responsibilities.argmax()
        # picks the actual component used to generate the observations.
        g.means_ = 20 * self.means
        g.covars_ = np.maximum(self.covars[self.covariance_type], 0.1)
        g.weights_ = self.weights

        with ignore_warnings(category=DeprecationWarning):
            samples = g.sample(n)
        self.assertEqual(samples.shape, (n, self.n_features))

    # This function tests the deprecated old GMM class
    @ignore_warnings(category=DeprecationWarning)
    def test_train(self, params='wmc'):
        g = mixture.GMM(n_components=self.n_components,
                        covariance_type=self.covariance_type)
        with ignore_warnings(category=DeprecationWarning):
            g.weights_ = self.weights
            g.means_ = self.means
            g.covars_ = 20 * self.covars[self.covariance_type]

        # Create a training set by sampling from the predefined distribution.
        with ignore_warnings(category=DeprecationWarning):
            X = g.sample(n_samples=100)
            g = self.model(n_components=self.n_components,
                           covariance_type=self.covariance_type,
                           random_state=rng, min_covar=1e-1,
                           n_iter=1, init_params=params)
            g.fit(X)

        # Do one training iteration at a time so we can keep track of
        # the log likelihood to make sure that it increases after each
        # iteration.
        trainll = []
        with ignore_warnings(category=DeprecationWarning):
            for _ in range(5):
                g.params = params
                g.init_params = ''
                g.fit(X)
                trainll.append(self.score(g, X))
            g.n_iter = 10
            g.init_params = ''
            g.params = params
            g.fit(X)  # finish fitting

        # Note that the log likelihood will sometimes decrease by a
        # very small amount after it has more or less converged due to
        # the addition of min_covar to the covariance (to prevent
        # underflow).  This is why the threshold is set to -0.5
        # instead of 0.
        with ignore_warnings(category=DeprecationWarning):
            delta_min = np.diff(trainll).min()
        self.assertTrue(
            delta_min > self.threshold,
            "The min nll increase is %f which is lower than the admissible"
            " threshold of %f, for model %s. The likelihoods are %s."
            % (delta_min, self.threshold, self.covariance_type, trainll))

    # This function tests the deprecated old GMM class
    @ignore_warnings(category=DeprecationWarning)
    def test_train_degenerate(self, params='wmc'):
        # Train on degenerate data with 0 in some dimensions
        # Create a training set by sampling from the predefined
        # distribution.
        X = rng.randn(100, self.n_features)
        X.T[1:] = 0
        g = self.model(n_components=2,
                       covariance_type=self.covariance_type,
                       random_state=rng, min_covar=1e-3, n_iter=5,
                       init_params=params)
        with ignore_warnings(category=DeprecationWarning):
            g.fit(X)
            trainll = g.score(X)
        self.assertTrue(np.sum(np.abs(trainll / 100 / X.shape[1])) < 5)

    # This function tests the deprecated old GMM class
    @ignore_warnings(category=DeprecationWarning)
    def test_train_1d(self, params='wmc'):
        # Train on 1-D data
        # Create a training set by sampling from the predefined
        # distribution.
        X = rng.randn(100, 1)
        # X.T[1:] = 0
        g = self.model(n_components=2,
                       covariance_type=self.covariance_type,
                       random_state=rng, min_covar=1e-7, n_iter=5,
                       init_params=params)
        with ignore_warnings(category=DeprecationWarning):
            g.fit(X)
            trainll = g.score(X)
            if isinstance(g, mixture.dpgmm._DPGMMBase):
                self.assertTrue(np.sum(np.abs(trainll / 100)) < 5)
            else:
                self.assertTrue(np.sum(np.abs(trainll / 100)) < 2)

    # This function tests the deprecated old GMM class
    @ignore_warnings(category=DeprecationWarning)
    def score(self, g, X):
        with ignore_warnings(category=DeprecationWarning):
            return g.score(X).sum()
