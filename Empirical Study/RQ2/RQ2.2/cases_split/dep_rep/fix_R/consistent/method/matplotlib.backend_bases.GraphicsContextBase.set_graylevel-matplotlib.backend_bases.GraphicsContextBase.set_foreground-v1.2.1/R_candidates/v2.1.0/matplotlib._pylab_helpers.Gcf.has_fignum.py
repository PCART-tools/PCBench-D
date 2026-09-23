    @classmethod
    def has_fignum(cls, num):
        """
        Return *True* if figure *num* exists.
        """
        return num in cls.figs
