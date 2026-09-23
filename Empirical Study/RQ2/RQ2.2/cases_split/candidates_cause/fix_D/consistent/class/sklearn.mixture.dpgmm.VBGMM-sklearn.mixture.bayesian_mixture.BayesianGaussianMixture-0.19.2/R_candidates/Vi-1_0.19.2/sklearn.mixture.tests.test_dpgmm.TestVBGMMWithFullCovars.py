class TestVBGMMWithFullCovars(unittest.TestCase, VBGMMTester):
    covariance_type = 'full'
    setUp = GMMTester._setUp
