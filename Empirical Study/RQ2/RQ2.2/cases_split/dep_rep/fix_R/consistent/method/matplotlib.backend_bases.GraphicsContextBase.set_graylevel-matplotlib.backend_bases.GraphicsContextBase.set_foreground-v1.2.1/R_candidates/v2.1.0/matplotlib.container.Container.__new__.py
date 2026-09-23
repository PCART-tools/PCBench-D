    def __new__(cls, *kl, **kwargs):
        return tuple.__new__(cls, kl[0])
