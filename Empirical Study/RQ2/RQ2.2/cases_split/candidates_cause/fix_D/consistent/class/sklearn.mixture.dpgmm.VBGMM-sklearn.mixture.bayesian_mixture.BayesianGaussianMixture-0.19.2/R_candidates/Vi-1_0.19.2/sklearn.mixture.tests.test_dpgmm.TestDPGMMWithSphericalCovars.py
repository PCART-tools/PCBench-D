class TestDPGMMWithSphericalCovars(unittest.TestCase, DPGMMTester):
    covariance_type = 'spherical'
    setUp = GMMTester._setUp
