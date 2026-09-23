    def center(self, x):
        '''
        center and optionally standardize the data using the mean and sigma
        from training set a
        '''
        if self.standardize:
            return (x - self.mu)/self.sigma
        else:
            return (x - self.mu)
