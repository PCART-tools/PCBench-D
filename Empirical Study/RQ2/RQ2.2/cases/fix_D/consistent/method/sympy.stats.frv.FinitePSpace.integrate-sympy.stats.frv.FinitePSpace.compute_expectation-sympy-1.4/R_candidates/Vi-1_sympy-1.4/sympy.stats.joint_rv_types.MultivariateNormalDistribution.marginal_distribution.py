    def marginal_distribution(self, indices, sym):
        sym = ImmutableMatrix([Indexed(sym, i) for i in indices])
        _mu, _sigma = self.mu, self.sigma
        k = len(self.mu)
        for i in range(k):
            if i not in indices:
                _mu = _mu.row_del(i)
                _sigma = _sigma.col_del(i)
                _sigma = _sigma.row_del(i)
        return Lambda(sym, S(1)/sqrt((2*pi)**(len(_mu))*det(_sigma))*exp(
            -S(1)/2*(_mu - sym).transpose()*(_sigma.inv()*\
                (_mu - sym)))[0])
