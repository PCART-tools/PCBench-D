    def check(self, mu, sigma):
        _value_check(len(mu) == len(sigma.col(0)),
            "Size of the mean vector and covariance matrix are incorrect.")
        #check if covariance matrix is positive definite or not.
        _value_check(all([Gt(i, 0) != False for i in sigma.eigenvals().keys()]),
            "The covariance matrix must be positive definite. ")
