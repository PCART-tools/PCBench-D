def test_load_sample_image():
    try:
        china = load_sample_image('china.jpg')
        assert_equal(china.dtype, 'uint8')
        assert_equal(china.shape, (427, 640, 3))
    except ImportError:
        warnings.warn("Could not load sample images, PIL is not available.")
