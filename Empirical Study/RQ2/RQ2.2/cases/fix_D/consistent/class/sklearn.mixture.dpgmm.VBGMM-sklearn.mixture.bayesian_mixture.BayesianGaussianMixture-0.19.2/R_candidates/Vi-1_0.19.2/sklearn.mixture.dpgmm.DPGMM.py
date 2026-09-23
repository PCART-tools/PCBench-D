@deprecated("The `DPGMM` class is not working correctly and it's better "
            "to use `sklearn.mixture.BayesianGaussianMixture` class with "
            "parameter `weight_concentration_prior_type='dirichlet_process'` "
            "instead. DPGMM is deprecated in 0.18 and will be "
            "removed in 0.20.")
class DPGMM(_DPGMMBase):
    """Dirichlet Process Gaussian Mixture Models

    .. deprecated:: 0.18
        This class will be removed in 0.20.
        Use :class:`sklearn.mixture.BayesianGaussianMixture` with
        parameter ``weight_concentration_prior_type='dirichlet_process'``
        instead.

    """

    def __init__(self, n_components=1, covariance_type='diag', alpha=1.0,
                 random_state=None, tol=1e-3, verbose=0, min_covar=None,
                 n_iter=10, params='wmc', init_params='wmc'):
        super(DPGMM, self).__init__(
            n_components=n_components, covariance_type=covariance_type,
            alpha=alpha, random_state=random_state, tol=tol, verbose=verbose,
            min_covar=min_covar, n_iter=n_iter, params=params,
            init_params=init_params)
