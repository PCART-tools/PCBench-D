    @staticmethod
    def null():
        """
        (staticmethod) Create a new null :class:`Bbox` from (inf, inf) to
        (-inf, -inf).
        """
        return Bbox(np.array([[np.inf, np.inf], [-np.inf, -np.inf]], float))
