    def feqcon(x, b=1):
        """ Equality constraint """
        return array([x[0]**2 + x[1] - b])
