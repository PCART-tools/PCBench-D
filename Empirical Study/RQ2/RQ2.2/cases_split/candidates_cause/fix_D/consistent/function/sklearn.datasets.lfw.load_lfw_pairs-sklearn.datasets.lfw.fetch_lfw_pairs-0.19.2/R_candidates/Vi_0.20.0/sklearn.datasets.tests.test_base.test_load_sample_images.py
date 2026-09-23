def test_load_sample_images():
    try:
        res = load_sample_images()
        assert_equal(len(res.images), 2)
        assert_equal(len(res.filenames), 2)
        assert_true(res.DESCR)
    except ImportError:
        warnings.warn("Could not load sample images, PIL is not available.")
