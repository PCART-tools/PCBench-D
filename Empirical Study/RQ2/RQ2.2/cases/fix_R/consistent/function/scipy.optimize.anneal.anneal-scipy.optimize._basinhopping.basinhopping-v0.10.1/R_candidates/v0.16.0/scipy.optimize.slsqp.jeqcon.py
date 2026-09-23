    def jeqcon(x, b=1):
        """ Jacobian of equality constraint """
        return array([[2*x[0], 1]])
