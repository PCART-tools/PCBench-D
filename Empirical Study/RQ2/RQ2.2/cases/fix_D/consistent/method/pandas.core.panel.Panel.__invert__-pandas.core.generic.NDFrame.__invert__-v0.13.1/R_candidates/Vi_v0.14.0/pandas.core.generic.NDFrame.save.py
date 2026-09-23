    def save(self, path):  # TODO remove in 0.14
        "Deprecated. Use to_pickle instead"
        import warnings
        from pandas.io.pickle import to_pickle
        warnings.warn("save is deprecated, use to_pickle", FutureWarning)
        return to_pickle(self, path)
