    @classmethod
    def construct(cls, **values):
        """
        Creates a new model and set __values__ without any validation, thus values should already be trusted.
        Chances are you don't want to use this method directly.
        """
        m = cls.__new__(cls)
        m.__setstate__(values)
        return m
