    def absorbing_probabilites(self):
        """
        Computes the absorbing probabilities, i.e.,
        the ij-th entry of the matrix denotes the
        probability of Markov chain being absorbed
        in state j starting from state i.
        """
        R = self._transient2absorbing()
        N = self.fundamental_matrix()
        if R == None or N == None:
            return None
        return N*R
