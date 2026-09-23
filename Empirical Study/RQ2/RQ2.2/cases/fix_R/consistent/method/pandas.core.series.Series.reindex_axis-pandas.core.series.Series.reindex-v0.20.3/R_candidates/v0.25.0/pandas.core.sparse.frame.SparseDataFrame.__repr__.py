    def __repr__(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", "Sparse")
            return super().__repr__()
