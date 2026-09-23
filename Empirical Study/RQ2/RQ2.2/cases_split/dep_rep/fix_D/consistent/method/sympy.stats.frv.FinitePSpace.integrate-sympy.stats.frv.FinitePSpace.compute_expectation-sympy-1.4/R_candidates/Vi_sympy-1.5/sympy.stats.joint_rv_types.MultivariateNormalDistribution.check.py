    @staticmethod
    def check(mu, sigma):
        _value_check(mu.shape[0] == sigma.shape[0],
            "Size of the mean vector and covariance matrix are incorrect.")
        #check if covariance matrix is positive definite or not.
        if not isinstance(sigma, MatrixSymbol):
            _value_check(sigma.is_positive_definite,
            "The covariance matrix must be positive definite. ")
