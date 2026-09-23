class TestDPGMMWithTiedCovars(unittest.TestCase, DPGMMTester):
    covariance_type = 'tied'
    setUp = GMMTester._setUp
