class TestGMMWithDiagonalCovars(unittest.TestCase, GMMTester):
    covariance_type = 'diag'
    model = mixture.GMM
    setUp = GMMTester._setUp
