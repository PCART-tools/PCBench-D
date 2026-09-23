    def sample(self):
        def search(x, y, u):
            while x < y:
                mid = (x + y)//2
                if u <= self.cdf(mid):
                    y = mid
                else:
                    x = mid + 1
            return x

        u = random.uniform(0, 1)
        if u <= self.cdf(S.Zero):
            return S.Zero
        n = S.One
        while True:
            if u > self.cdf(2*n):
                n *= 2
            else:
                return search(n, 2*n, u)
