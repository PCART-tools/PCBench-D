@_api.deprecated("3.6", alternative="a vendored copy of the existing code, "
                 "including the private function _cleanup_cm")
class CleanupTestCase(unittest.TestCase):
    """A wrapper for unittest.TestCase that includes cleanup operations."""
    @classmethod
    def setUpClass(cls):
        cls._cm = _cleanup_cm().__enter__()

    @classmethod
    def tearDownClass(cls):
        cls._cm.__exit__(None, None, None)
