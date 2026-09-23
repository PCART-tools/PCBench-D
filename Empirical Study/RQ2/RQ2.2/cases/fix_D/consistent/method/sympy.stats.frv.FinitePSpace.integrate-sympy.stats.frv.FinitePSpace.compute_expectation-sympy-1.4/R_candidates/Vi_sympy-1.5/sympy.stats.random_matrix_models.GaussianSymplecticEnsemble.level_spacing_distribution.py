    def level_spacing_distribution(self):
        s = Dummy('s')
        f = ((S(2)**18)/((S(3)**6)*(pi**3)))*(s**4)*exp((-64/(9*pi))*s**2)
        return Lambda(s, f)
