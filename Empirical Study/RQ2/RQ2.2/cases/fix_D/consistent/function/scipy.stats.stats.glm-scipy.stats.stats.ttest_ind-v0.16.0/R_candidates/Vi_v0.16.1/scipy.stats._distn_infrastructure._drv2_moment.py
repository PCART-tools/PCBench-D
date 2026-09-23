def _drv2_moment(self, n, *args):
    """Non-central moment of discrete distribution."""
    # many changes, originally not even a return
    tot = 0.0
    diff = 1e100
    # pos = self.a
    pos = max(0.0, 1.0*self.a)
    count = 0
    # handle cases with infinite support
    ulimit = max(1000, (min(self.b, 1000) + max(self.a, -1000))/2.0)
    llimit = min(-1000, (min(self.b, 1000) + max(self.a, -1000))/2.0)

    while (pos <= self.b) and ((pos <= ulimit) or
                               (diff > self.moment_tol)):
        diff = np.power(pos, n) * self.pmf(pos, *args)
        # use pmf because _pmf does not check support in randint and there
        # might be problems ? with correct self.a, self.b at this stage
        tot += diff
        pos += self.inc
        count += 1

    if self.a < 0:  # handle case when self.a = -inf
        diff = 1e100
        pos = -self.inc
        while (pos >= self.a) and ((pos >= llimit) or
                                   (diff > self.moment_tol)):
            diff = np.power(pos, n) * self.pmf(pos, *args)
            # using pmf instead of _pmf, see above
            tot += diff
            pos -= self.inc
            count += 1
    return tot
