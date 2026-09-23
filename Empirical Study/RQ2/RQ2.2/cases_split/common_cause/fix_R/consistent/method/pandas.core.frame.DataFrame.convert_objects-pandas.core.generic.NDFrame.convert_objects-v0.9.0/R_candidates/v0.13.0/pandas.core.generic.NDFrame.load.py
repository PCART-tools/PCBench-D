    def load(self, path):  # TODO remove in 0.14
        "Deprecated. Use read_pickle instead."
        import warnings
        from pandas.io.pickle import read_pickle
        warnings.warn("load is deprecated, use pd.read_pickle", FutureWarning)
        return read_pickle(path)
