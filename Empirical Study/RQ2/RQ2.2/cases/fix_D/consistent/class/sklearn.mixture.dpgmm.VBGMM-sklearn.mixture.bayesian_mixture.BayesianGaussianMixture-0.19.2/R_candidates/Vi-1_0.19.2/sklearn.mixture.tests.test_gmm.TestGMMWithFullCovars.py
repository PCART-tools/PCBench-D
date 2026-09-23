class TestGMMWithFullCovars(unittest.TestCase, GMMTester):
    covariance_type = 'full'
    model = mixture.GMM
    setUp = GMMTester._setUp
