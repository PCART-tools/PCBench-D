@deprecated("The `VBGMM` class is not working correctly and it's better "
            "to use `sklearn.mixture.BayesianGaussianMixture` class with "
            "parameter `weight_concentration_prior_type="
            "'dirichlet_distribution'` instead. "
            "VBGMM is deprecated in 0.18 and will be removed in 0.20.")
class VBGMM(_DPGMMBase):
    """Variational Inference for the Gaussian Mixture Model

    .. deprecated:: 0.18
        This class will be removed in 0.20.
        Use :class:`sklearn.mixture.BayesianGaussianMixture` with parameter
        ``weight_concentration_prior_type='dirichlet_distribution'`` instead.

    Variational inference for a Gaussian mixture model probability
    distribution. This class allows for easy and efficient inference
    of an approximate posterior distribution over the parameters of a
    Gaussian mixture model with a fixed number of components.

    Initialization is with normally-distributed means and identity
    covariance, for proper convergence.

    Read more in the :ref:`User Guide <bgmm>`.

    Parameters
    ----------
    n_components : int, default 1
        Number of mixture components.

    covariance_type : string, default 'diag'
        String describing the type of covariance parameters to
        use.  Must be one of 'spherical', 'tied', 'diag', 'full'.

    alpha : float, default 1
        Real number representing the concentration parameter of
        the dirichlet distribution. Intuitively, the higher the
        value of alpha the more likely the variational mixture of
        Gaussians model will use all components it can.

    tol : float, default 1e-3
        Convergence threshold.

    n_iter : int, default 10
        Maximum number of iterations to perform before convergence.

    params : string, default 'wmc'
        Controls which parameters are updated in the training
        process.  Can contain any combination of 'w' for weights,
        'm' for means, and 'c' for covars.

    init_params : string, default 'wmc'
        Controls which parameters are updated in the initialization
        process.  Can contain any combination of 'w' for weights,
        'm' for means, and 'c' for covars.  Defaults to 'wmc'.

    verbose : int, default 0
        Controls output verbosity.

    Attributes
    ----------
    covariance_type : string
        String describing the type of covariance parameters used by
        the DP-GMM.  Must be one of 'spherical', 'tied', 'diag', 'full'.

    n_features : int
        Dimensionality of the Gaussians.

    n_components : int (read-only)
        Number of mixture components.

    weights_ : array, shape (`n_components`,)
        Mixing weights for each mixture component.

    means_ : array, shape (`n_components`, `n_features`)
        Mean parameters for each mixture component.

    precs_ : array
        Precision (inverse covariance) parameters for each mixture
        component.  The shape depends on `covariance_type`::

            (`n_components`, 'n_features')                if 'spherical',
            (`n_features`, `n_features`)                  if 'tied',
            (`n_components`, `n_features`)                if 'diag',
            (`n_components`, `n_features`, `n_features`)  if 'full'

    converged_ : bool
        True when convergence was reached in fit(), False
        otherwise.

    See Also
    --------
    GMM : Finite Gaussian mixture model fit with EM
    DPGMM : Infinite Gaussian mixture model, using the dirichlet
        process, fit with a variational algorithm
    """

    def __init__(self, n_components=1, covariance_type='diag', alpha=1.0,
                 random_state=None, tol=1e-3, verbose=0,
                 min_covar=None, n_iter=10, params='wmc', init_params='wmc'):
        super(VBGMM, self).__init__(
            n_components, covariance_type, random_state=random_state,
            tol=tol, verbose=verbose, min_covar=min_covar,
            n_iter=n_iter, params=params, init_params=init_params)
        self.alpha = alpha

    def _fit(self, X, y=None):
        """Estimate model parameters with the variational algorithm.

        For a full derivation and description of the algorithm see
        doc/modules/dp-derivation.rst
        or
        http://scikit-learn.org/stable/modules/dp-derivation.html

        A initialization step is performed before entering the EM
        algorithm. If you want to avoid this step, set the keyword
        argument init_params to the empty string '' when creating
        the object. Likewise, if you just would like to do an
        initialization, set n_iter=0.

        Parameters
        ----------
        X : array_like, shape (n, n_features)
            List of n_features-dimensional data points.  Each row
            corresponds to a single data point.

        Returns
        -------
        responsibilities : array, shape (n_samples, n_components)
            Posterior probabilities of each mixture component for each
            observation.
        """
        self.alpha_ = float(self.alpha) / self.n_components
        return super(VBGMM, self)._fit(X, y)

    def score_samples(self, X):
        """Return the likelihood of the data under the model.

        Compute the bound on log probability of X under the model
        and return the posterior distribution (responsibilities) of
        each mixture component for each element of X.

        This is done by computing the parameters for the mean-field of
        z for each observation.

        Parameters
        ----------
        X : array_like, shape (n_samples, n_features)
            List of n_features-dimensional data points.  Each row
            corresponds to a single data point.

        Returns
        -------
        logprob : array_like, shape (n_samples,)
            Log probabilities of each data point in X
        responsibilities : array_like, shape (n_samples, n_components)
            Posterior probabilities of each mixture component for each
            observation
        """
        check_is_fitted(self, 'gamma_')

        X = check_array(X)
        if X.ndim == 1:
            X = X[:, np.newaxis]
        dg = digamma(self.gamma_) - digamma(np.sum(self.gamma_))

        if self.covariance_type not in ['full', 'tied', 'diag', 'spherical']:
            raise NotImplementedError("This ctype is not implemented: %s"
                                      % self.covariance_type)
        p = _bound_state_log_lik(X, self._initial_bound + self.bound_prec_,
                                 self.precs_, self.means_,
                                 self.covariance_type)

        z = p + dg
        z = log_normalize(z, axis=-1)
        bound = np.sum(z * p, axis=-1)
        return bound, z

    def _update_concentration(self, z):
        for i in range(self.n_components):
            self.gamma_[i] = self.alpha_ + np.sum(z.T[i])

    def _initialize_gamma(self):
        self.gamma_ = self.alpha_ * np.ones(self.n_components)

    def _bound_proportions(self, z):
        logprior = 0.
        dg = digamma(self.gamma_)
        dg -= digamma(np.sum(self.gamma_))
        logprior += np.sum(dg.reshape((-1, 1)) * z.T)
        z_non_zeros = z[z > np.finfo(np.float32).eps]
        logprior -= np.sum(z_non_zeros * np.log(z_non_zeros))
        return logprior

    def _bound_concentration(self):
        logprior = 0.
        logprior = gammaln(np.sum(self.gamma_)) - gammaln(self.n_components
                                                          * self.alpha_)
        logprior -= np.sum(gammaln(self.gamma_) - gammaln(self.alpha_))
        sg = digamma(np.sum(self.gamma_))
        logprior += np.sum((self.gamma_ - self.alpha_)
                           * (digamma(self.gamma_) - sg))
        return logprior

    def _monitor(self, X, z, n, end=False):
        """Monitor the lower bound during iteration

        Debug method to help see exactly when it is failing to converge as
        expected.

        Note: this is very expensive and should not be used by default."""
        if self.verbose > 0:
            print("Bound after updating %8s: %f" % (n, self.lower_bound(X, z)))
            if end:
                print("Cluster proportions:", self.gamma_)
                print("covariance_type:", self.covariance_type)

    def _set_weights(self):
        self.weights_[:] = self.gamma_
        self.weights_ /= np.sum(self.weights_)
