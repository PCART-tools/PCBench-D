    def to_pickle(self, path):
        """
        Pickle (serialize) object to input file path

        Parameters
        ----------
        path : string
            File path
        """
        from pandas.io.pickle import to_pickle
        return to_pickle(self, path)
