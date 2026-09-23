def test_load_missing_sample_image_error():
    if pillow_installed:
        assert_raises(AttributeError, load_sample_image,
                      'blop.jpg')
    else:
        warnings.warn("Could not load sample images, PIL is not available.")
