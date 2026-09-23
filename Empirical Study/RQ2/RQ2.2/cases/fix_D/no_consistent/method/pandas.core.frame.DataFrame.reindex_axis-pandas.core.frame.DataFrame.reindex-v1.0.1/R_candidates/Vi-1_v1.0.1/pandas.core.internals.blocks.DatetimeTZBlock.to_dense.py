    def to_dense(self):
        # we request M8[ns] dtype here, even though it discards tzinfo,
        # as lots of code (e.g. anything using values_from_object)
        # expects that behavior.
        return np.asarray(self.values, dtype=_NS_DTYPE)
