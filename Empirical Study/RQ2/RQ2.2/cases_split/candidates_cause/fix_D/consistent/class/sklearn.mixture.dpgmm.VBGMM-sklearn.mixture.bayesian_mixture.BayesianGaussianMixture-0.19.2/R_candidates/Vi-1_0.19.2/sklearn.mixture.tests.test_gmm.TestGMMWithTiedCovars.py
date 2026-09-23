class TestGMMWithTiedCovars(unittest.TestCase, GMMTester):
    covariance_type = 'tied'
    model = mixture.GMM
    setUp = GMMTester._setUp
