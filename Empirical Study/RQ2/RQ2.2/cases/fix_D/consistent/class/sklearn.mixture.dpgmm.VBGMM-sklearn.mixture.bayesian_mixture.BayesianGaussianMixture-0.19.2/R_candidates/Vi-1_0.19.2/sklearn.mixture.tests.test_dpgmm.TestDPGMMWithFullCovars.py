class TestDPGMMWithFullCovars(unittest.TestCase, DPGMMTester):
    covariance_type = 'full'
    setUp = GMMTester._setUp
