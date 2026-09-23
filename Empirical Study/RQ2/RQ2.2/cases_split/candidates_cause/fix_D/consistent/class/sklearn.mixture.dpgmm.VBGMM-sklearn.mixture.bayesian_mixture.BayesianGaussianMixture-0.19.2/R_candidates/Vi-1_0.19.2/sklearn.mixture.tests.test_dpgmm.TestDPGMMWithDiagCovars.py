class TestDPGMMWithDiagCovars(unittest.TestCase, DPGMMTester):
    covariance_type = 'diag'
    setUp = GMMTester._setUp
