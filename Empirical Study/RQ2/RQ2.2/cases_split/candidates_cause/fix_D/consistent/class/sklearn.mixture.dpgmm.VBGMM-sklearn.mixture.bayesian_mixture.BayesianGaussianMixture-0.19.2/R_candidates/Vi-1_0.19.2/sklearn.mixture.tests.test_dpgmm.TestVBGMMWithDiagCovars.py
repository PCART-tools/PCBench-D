class TestVBGMMWithDiagCovars(unittest.TestCase, VBGMMTester):
    covariance_type = 'diag'
    setUp = GMMTester._setUp
