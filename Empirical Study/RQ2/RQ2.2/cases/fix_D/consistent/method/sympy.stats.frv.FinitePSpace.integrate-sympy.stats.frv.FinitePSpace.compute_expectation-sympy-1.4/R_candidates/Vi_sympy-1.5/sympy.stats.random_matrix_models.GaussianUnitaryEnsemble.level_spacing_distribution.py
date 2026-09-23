    def level_spacing_distribution(self):
        s = Dummy('s')
        f = (32/pi**2)*(s**2)*exp((-4/pi)*s**2)
        return Lambda(s, f)
