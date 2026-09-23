    def fundamental_matrix(self):
        Q = self._transient2transient()
        if Q == None:
            return None
        I = eye(Q.shape[0])
        if (I - Q).det() == 0:
            raise ValueError("Fundamental matrix doesn't exists.")
        return ImmutableMatrix((I - Q).inv().tolist())
