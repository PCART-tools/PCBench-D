    def __new__(cls, a, s=1, m=0):
        a, s, m = list(map(sympify, (a, s, m)))
        return Basic.__new__(cls, a, s, m)
