    def level_spacing_distribution(self):
        s = Dummy('s')
        f = (pi/2)*s*exp((-pi/4)*s**2)
        return Lambda(s, f)
