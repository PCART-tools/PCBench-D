def make_random_dense_gaussian_matrix(n_rows, n_columns, mu=0, sigma=0.01):
    """
    Make some random data with Gaussian distributed values
    """
    np.random.seed(142352345)
    res = np.random.normal(mu, sigma, n_rows*n_columns)
    return np.reshape(res, (n_rows, n_columns))
