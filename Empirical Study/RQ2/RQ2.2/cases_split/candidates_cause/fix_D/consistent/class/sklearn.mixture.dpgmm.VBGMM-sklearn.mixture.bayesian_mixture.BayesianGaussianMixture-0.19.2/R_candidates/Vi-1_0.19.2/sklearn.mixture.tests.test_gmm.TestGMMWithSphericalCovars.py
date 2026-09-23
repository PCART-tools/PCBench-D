class TestGMMWithSphericalCovars(unittest.TestCase, GMMTester):
    covariance_type = 'spherical'
    model = mixture.GMM
    setUp = GMMTester._setUp
