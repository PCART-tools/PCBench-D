        def __call__(self, x, pos=None):
            degrees = (x / np.pi) * 180.0
            degrees = np.round(degrees / self._round_to) * self._round_to
            if rcParams['text.usetex'] and not rcParams['text.latex.unicode']:
                return r"$%0.0f^\circ$" % degrees
            else:
                return "%0.0f\N{DEGREE SIGN}" % degrees
