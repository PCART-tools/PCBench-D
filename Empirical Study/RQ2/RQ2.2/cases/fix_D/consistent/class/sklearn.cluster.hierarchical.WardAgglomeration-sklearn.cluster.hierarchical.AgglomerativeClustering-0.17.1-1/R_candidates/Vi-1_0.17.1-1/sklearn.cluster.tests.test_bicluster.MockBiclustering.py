class MockBiclustering(BaseEstimator, BiclusterMixin):
    # Mock object for testing get_submatrix.
    def __init__(self):
        pass

    def get_indices(self, i):
        # Overridden to reproduce old get_submatrix test.
        return (np.where([True, True, False, False, True])[0],
                np.where([False, False, True, True])[0])
