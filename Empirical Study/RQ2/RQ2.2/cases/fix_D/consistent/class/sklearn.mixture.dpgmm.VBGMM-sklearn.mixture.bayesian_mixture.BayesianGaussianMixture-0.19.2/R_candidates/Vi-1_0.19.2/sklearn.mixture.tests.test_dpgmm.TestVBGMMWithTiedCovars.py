class TestVBGMMWithTiedCovars(unittest.TestCase, VBGMMTester):
    covariance_type = 'tied'
    setUp = GMMTester._setUp
