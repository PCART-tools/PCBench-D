    def _values_for_factorize(self):
        # Still override this for hash_pandas_object
        return np.asarray(self), self.fill_value
