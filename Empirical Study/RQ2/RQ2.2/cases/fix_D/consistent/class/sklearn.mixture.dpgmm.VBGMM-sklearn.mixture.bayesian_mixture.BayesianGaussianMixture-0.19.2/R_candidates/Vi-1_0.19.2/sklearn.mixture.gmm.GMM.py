@deprecated("The class GMM is deprecated in 0.18 and will be "
            " removed in 0.20. Use class GaussianMixture instead.")
class GMM(_GMMBase):
    """
    Legacy Gaussian Mixture Model

    .. deprecated:: 0.18
        This class will be removed in 0.20.
        Use :class:`sklearn.mixture.GaussianMixture` instead.

    """

    def __init__(self, n_components=1, covariance_type='diag',
                 random_state=None, tol=1e-3, min_covar=1e-3,
                 n_iter=100, n_init=1, params='wmc', init_params='wmc',
                 verbose=0):
        super(GMM, self).__init__(
            n_components=n_components, covariance_type=covariance_type,
            random_state=random_state, tol=tol, min_covar=min_covar,
            n_iter=n_iter, n_init=n_init, params=params,
            init_params=init_params, verbose=verbose)
