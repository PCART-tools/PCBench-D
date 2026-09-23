class TestVBGMMWithSphericalCovars(unittest.TestCase, VBGMMTester):
    covariance_type = 'spherical'
    setUp = GMMTester._setUp
